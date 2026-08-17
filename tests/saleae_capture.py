from saleae import automation
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "test-results" / "saleae"

OUT.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("SALEAE CAPTURE")
print("=" * 60)

print("Connecting to Logic 2 on port 10430...")

with automation.Manager.connect(port=10430) as manager:

    print("Connected to Logic 2.")
    print("Logic 2:", manager.get_app_info())

    devices = manager.get_devices()

    print("Devices found:")
    for device in devices:
        print(device)

    real_devices = [d for d in devices if not d.is_simulation]

    if not real_devices:
        raise RuntimeError(
            "No physical Saleae device found."
        )

    device = real_devices[0]

    print("Using device:", device)

    # Saleae device supports 8 MHz.
    # Do not specify digital_threshold_volts.
    device_configuration = automation.LogicDeviceConfiguration(
        enabled_digital_channels=[0],
        digital_sample_rate=8_000_000,
    )

    capture_configuration = automation.CaptureConfiguration(
        capture_mode=automation.TimedCaptureMode(
            duration_seconds=5.0
        )
    )

    print("Starting 5 second capture...")
    print("CH0 -> STM32 PA5 / User LED")
    print("GND -> STM32 GND")

    with manager.start_capture(
        device_id=device.device_id,
        device_configuration=device_configuration,
        capture_configuration=capture_configuration,
    ) as capture:

        capture.wait()

        print("Capture completed.")

        capture.export_raw_data_csv(
            directory=str(OUT),
            digital_channels=[0]
        )

        capture_path = OUT / "stm32_led_capture.sal"
        capture.save_capture(str(capture_path))

        print("Saved:", capture_path)

print("SALEAE CAPTURE COMPLETE")