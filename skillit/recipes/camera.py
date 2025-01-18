"""Example script to interact with the robot's camera using WebRTC.

NOTE: This script is currently untested.
"""

import asyncio
import base64
import logging

import cv2  # type: ignore[import-not-found]
import requests
from aiortc import (  # type: ignore[import-untyped]
    MediaStreamTrack,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
)

logging.getLogger("ffmpeg").setLevel(logging.ERROR)

# Server URL (replace with your actual server URL)
SERVER_URL = "http://192.168.42.1:8083/stream/s1/channel/0/webrtc?uuid=s1&channel=0"

i = 0


# Video Display Track
class VideoDisplay(VideoStreamTrack):
    def __init__(self, track: MediaStreamTrack) -> None:
        """Initialize the video display track.

        Args:
            track: The source video track to display.
        """
        super().__init__()
        self.track = track

    async def recv(self) -> MediaStreamTrack:
        """Receive and process a video frame.

        Returns:
            The processed video frame.

        Raises:
            Exception: If there's an error processing the frame.
        """
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


async def create_sdp_offer(pc: RTCPeerConnection) -> str:
    """Create and encode an SDP offer.

    Args:
        pc: The peer connection to create the offer for.

    Returns:
        The base64 encoded SDP offer.
    """
    # Create an SDP offer
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    # Return the SDP offer as base64
    return base64.b64encode(pc.localDescription.sdp.encode("utf-8")).decode("utf-8")


def send_sdp_to_server(base64_sdp: str) -> str:
    """Send SDP offer to server and get answer.

    Args:
        base64_sdp: The base64 encoded SDP offer.

    Returns:
        The decoded SDP answer from the server.

    Raises:
        requests.exceptions.RequestException: If the server request fails.
    """
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


async def display_video(display: VideoDisplay) -> None:
    """Coroutine to continuously receive and display video frames.

    Args:
        display: The video display track to receive frames from.
    """
    try:
        while True:
            await display.recv()
    except Exception as e:
        print(f"Display video error: {e}")


async def main() -> None:
    """Main function to set up and run the WebRTC video stream."""
    pc = RTCPeerConnection()
    pc.addTransceiver("video", direction="recvonly")

    @pc.on("track")
    def on_track(track: MediaStreamTrack) -> None:
        """Handle incoming media tracks.

        Args:
            track: The received media track.
        """
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
