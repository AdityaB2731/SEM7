from pathlib import Path
import sys
import tempfile

SIGNATURES = {
    "jpg": {
        "start": bytes.fromhex("FFD8FF"),
        "end": bytes.fromhex("FFD9")
    },
    "png": {
        "start": bytes.fromhex("89504E470D0A1A0A"),
        "end": bytes.fromhex("49454E44AE426082")
    },
    "pdf": {
        "start": b"%PDF-",
        "end": b"%%EOF"
    }
}


def carve_files(image_path, output_folder):
    image_path = Path(image_path)
    output_folder = Path(output_folder)

    if not image_path.is_file():
        print("Error: Disk image not found.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)
    data = image_path.read_bytes()

    recovered = 0

    print("===== FILE RECOVERY REPORT =====")
    print("Image:", image_path)
    print("Image size:", len(data), "bytes")

    for extension, sig in SIGNATURES.items():
        start_sig = sig["start"]
        end_sig = sig["end"]
        position = 0

        while True:
            start = data.find(start_sig, position)

            if start == -1:
                break

            end = data.find(end_sig, start + len(start_sig))

            if end == -1:
                print(
                    f"Incomplete {extension.upper()} at offset {start}"
                )
                position = start + 1
                continue

            # Include the complete end marker
            end += len(end_sig)
            recovered += 1

            output_path = output_folder / (
                f"recovered_{recovered}.{extension}"
            )

            output_path.write_bytes(data[start:end])

            print(
                f"Recovered {extension.upper()} file: "
                f"{output_path} "
                f"(offset {start}, {end - start} bytes)"
            )

            position = end

    print("\nTotal files recovered:", recovered)
    print("Output folder:", output_folder.resolve())
    print("Validate recovered files before using them.")


def create_demo_image():
    demo_data = (
        b"SAFE SYNTHETIC FORENSIC IMAGE\n"
        b"\xff\xd8\xffSIMULATED JPEG CONTENT\xff\xd9\n"
        b"\x89PNG\r\n\x1a\nSIMULATED PNG CONTENT"
        b"IEND\xaeB`\x82\n"
        b"%PDF-1.4\nSIMULATED PDF CONTENT\n%%EOF\n"
    )
    demo_file = Path(tempfile.gettempdir()) / "csdf_demo_image.bin"
    demo_file.write_bytes(demo_data)
    return demo_file


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--demo":
        demo_image = create_demo_image()
        demo_output = Path("recovered_files_demo")
        carve_files(demo_image, demo_output)
        print("\nDemo complete: only synthetic data was used.")
    elif len(sys.argv) != 2:
        print("Safe file recovery demo")
        print("This program needs an existing forensic image file.")
        print("It scans the image for JPG, PNG, and PDF signatures.")
        print("It never reads a live disk unless you provide one as the argument.")
        print()
        print("Usage:")
        print("  python file_recovery.py <disk_image_file>")
        print("  python file_recovery.py --demo")
        print()
        print("Example with an authorized copied image:")
        print("  python file_recovery.py .\\test-image.dd")
    else:
        carve_files(sys.argv[1], "recovered_files")