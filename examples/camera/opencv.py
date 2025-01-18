import asyncio
import base64
import logging

import cv2
import requests
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack

logging.getLogger("ffmpeg").setLevel(logging.ERROR)

# Server URL (replace with your actual server URL)
SERVER_URL = "http://192.168.42.1:8083/stream/s1/channel/0/webrtc?uuid=s1&channel=0"

i = 0


# Video Display Track
class VideoDisplay(VideoStreamTrack):
    def __init__(self, track):
        super().__init__()
        self.track = track

    async def recv(self):
        try:
            frame = await self.track.recv()
            img = frame.to_ndarray(format="bgr24")
            # Do something with the frame, e.g. object detection
            cv2.imshow("WebRTC Video", img)
            cv2.waitKey(1)
            return frame
        except Exception as e:
            print(f"Error in recv: {e}")
            raise


async def create_sdp_offer(pc):
    # Create an SDP offer
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    # Return the SDP offer as base64
    return base64.b64encode(pc.localDescription.sdp.encode("utf-8")).decode("utf-8")


def send_sdp_to_server(base64_sdp):
    # Prepare headers and data
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
    }
    data = {"data": base64_sdp}

    # Send HTTP POST request
    response = requests.post(SERVER_URL, headers=headers, data=data, verify=False)
    response.raise_for_status()

    # Decode the base64 SDP answer from the server
    return base64.b64decode(response.text).decode("utf-8")


async def display_video(display):
    """Coroutine to continuously receive and display video frames"""
    try:
        while True:
            await display.recv()
    except Exception as e:
        print(f"Display video error: {e}")


async def main():
    pc = RTCPeerConnection()
    pc.addTransceiver("video", direction="recvonly")

    @pc.on("track")
    def on_track(track):
        if track.kind == "video":
            display = VideoDisplay(track)
            asyncio.ensure_future(display_video(display))

    # Create and set local description
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    # Send offer to server
    sdp_offer_base64 = base64.b64encode(pc.localDescription.sdp.encode("utf-8")).decode("utf-8")
    sdp_answer = send_sdp_to_server(sdp_offer_base64)

    # Set remote description
    await pc.setRemoteDescription(RTCSessionDescription(sdp=sdp_answer, type="answer"))

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        await pc.close()


if __name__ == "__main__":
    asyncio.run(main())
