import argparse
import dorky.dorky as dorky
from dorky import __about__ as about


def main():
    """Main cli function to start Dorky."""
    parser = argparse.ArgumentParser(description="Start Dorky")
    parser.add_argument("start", help="Start Dorky")
    # add port option
    parser.add_argument(
        "-p", "--port", type=int, default=8080, help="Port to run Dorky on (default: 8080)",
    )
    args = parser.parse_args()
    if args.start:
        print(f"\n⚙️ Starting Dorky v{about.__version__} on port {args.port}...")
        dorky.main(port=args.port)
