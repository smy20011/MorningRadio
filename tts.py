from kokoro_onnx import Kokoro
from pathlib import Path
from pydub import AudioSegment
import soundfile as sf
import argparse
import tempfile


def main():
    parser = argparse.ArgumentParser(
        description="Parse command-line arguments for model processing."
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Path to the input file or directory."
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to the output file or directory.",
    )
    args = parser.parse_args()

    kokoro = Kokoro("models/kokoro-v0_19.onnx", "models/voices.bin")
    samples, sample_rate = kokoro.create(
        Path(args.input).read_text(), voice="af_sarah", speed=1.0, lang="en-us"
    )

    wav_file = tempfile.mktemp(".wav")
    sf.write(wav_file, samples, samplerate=sample_rate)

    segment = AudioSegment.from_wav(wav_file)
    segment.export(args.output, format="mp3", bitrate="128k")


if __name__ == "__main__":
    main()
