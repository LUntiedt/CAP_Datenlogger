/*
 * CAP Datenlogger – Einstiegspunkt
 *
 * Firmware-Skelett zum Testen der Toolchain auf dem nRF54L15 DK.
 * Aufbau der Schichten: docs/architecture/firmware.md
 */

#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(main, LOG_LEVEL_INF);

int main(void)
{
	LOG_INF("CAP Datenlogger: Firmware-Skelett gestartet");

	while (1) {
		k_sleep(K_SECONDS(5));
		LOG_INF("lebt");
	}

	return 0;
}
