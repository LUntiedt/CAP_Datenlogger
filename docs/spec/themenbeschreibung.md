*Themenbeschreibung des ERTS Lab (Prof. Dr. Markus Cremer, TH Köln), wortgetreu übernommen. Die Seite wurde inzwischen von der Laborwebsite genommen.*

# Miniaturised Battery-Powered Acceleration Data Logger for Animal-Borne Field Measurements

A preceding research project on accelerometer-based animal health monitoring — activity classification, step counting, and ODBA/VeDBA activity metrics on an ST SensorTile.box PRO with an LSM6DSV16X IMU — established the algorithmic groundwork but ran into a hard practical limit: the evaluation board is far too large and too fragile to attach to a live animal. Every further step in this research thread depends on real acceleration data recorded on real animals, and that data cannot be collected with the hardware currently available.

This thesis closes that gap by developing a small, self-contained, battery-powered acceleration data logger ready for deployment in a zoo cooperation. The requirement is deliberately narrow: record raw acceleration data and recover it — no on-device classification, no live streaming. Everything else is subordinate to making the device small enough, light enough, and long-lived enough to sit on a collar or harness for a meaningful recording period.

The engineering substance of the work lies entirely in a multi-way design conflict: energy budget versus sampling rate, cell capacity versus physical size, and on-device storage capacity versus desired recording duration. These constraints are genuinely in tension. At 50 Hz across three axes at 16-bit resolution, raw data accumulates at roughly 26 MB per day — more than a typical serial NOR flash holds in its entirety. Resolving this conflict through informed choices about output data rate, sensor FIFO usage, duty cycling, storage technology, and data format is the core of the thesis.

## Objectives

- Derive a quantified requirements specification from the application: sampling rate, resolution, recording duration, maximum mass and dimensions — each justified against the needs of ODBA/VeDBA computation and gait periodicity analysis
- Design and manufacture a compact custom PCB integrating a low-power IMU, a BLE-capable MCU, non-volatile storage, and a coin cell holder in an animal-mountable form factor
- Implement firmware for continuous acquisition (sensor FIFO → flash), power management, and a BLE data download service
- Characterise the device: measured current consumption per operating state, achievable recording duration, storage throughput, and sampling timing consistency
- Validate the logger in a first practical recording, and deliver data in a form directly usable by the lab's ongoing algorithm work

## Starting Point

The preceding research project defines what the logger must deliver:

- ODBA and VeDBA require only raw tri-axial acceleration; sampling rates in the 25–100 Hz range are sufficient for both these metrics and for autocorrelation-based gait periodicity analysis
- The LSM6DSV16X is characterised and understood in the lab, and its integrated FIFO is central to a low-power acquisition architecture — buffering samples in the sensor lets the MCU sleep between burst transfers instead of waking per sample
- Existing recordings from the evaluation board provide a reference for signal quality against which the new device can be verified

The central design conflict can be stated concretely at the outset:

- At 50 Hz, 3 axes, 16 bit, raw data accrues at 300 B/s — about 26 MB per day; at 25 Hz roughly 13 MB, at 100 Hz roughly 52 MB
- A large serial NOR flash holds around 32 MB; NAND flash reaches into the hundreds of MB at the cost of bad-block management
- A CR2032 cell offers roughly 225 mAh, a CR2450 about 620 mAh at noticeably greater size; a seven-day runtime from a CR2032 permits an average current draw of about 1.3 mA, a thirty-day runtime about 0.3 mA
- Coin cells have high internal resistance and sag under the pulse load of BLE transmission — buffering capacitance is a design requirement, not an optional refinement

Reconciling these figures into a coherent, justified specification is the first substantial task of the thesis.

The ERTS Lab provides the development toolchain and expertise in low-power embedded design on Nordic platforms, PCB fabrication and assembly, and established methodology for current profiling. The Wuppertal Zoo cooperation provides the deployment context and the opportunity for a first real recording.

## Planned Approach

### 1. Requirements and component selection

- Derive concrete target values for sampling rate, resolution, recording duration, runtime, mass, and dimensions from the application requirements, and document the reasoning
- Evaluate IMU candidates against power consumption, FIFO capability, and package size; the LSM6DSV16X is the natural starting point given continuity with the preceding project, but the choice should be justified rather than assumed
- Select a BLE SoC with very low sleep current — the nRF52 class is the obvious candidate given existing lab experience
- Compare storage options: serial NOR versus NAND flash, weighed against capacity, write energy, and firmware complexity
- Analyse the cell trade-off: primary coin cell for maximum energy density and simplicity versus rechargeable for reusability, and select with justification

### 2. Hardware design

- Design a compact PCB carrying IMU, MCU, flash, cell holder, buffering capacitance, and a programming/debug interface
- Include a current measurement shunt to permit accurate power profiling of the assembled device
- Optimise the layout for minimal area and mass while retaining assembly feasibility and BLE antenna performance
- Manufacture and assemble the prototype
- Provide basic environmental protection appropriate to the deployment: a simple enclosure or conformal coating against moisture and mechanical stress; a fully sealed potted design is explicitly out of scope

### 3. Firmware development

- Implement the acquisition path: IMU FIFO configuration, burst readout on watermark interrupt, and buffered writes to flash
- Implement aggressive power management: MCU deep sleep between transfers, peripheral power gating, and BLE disabled entirely during recording
- Implement a BLE download service for data recovery, active only when the device is explicitly woken for readout
- Ensure sampling timing consistency and record timestamps that allow the data to be aligned with external observation — a synchronisation marker at recording start enables later correlation with video ground truth
- Define a compact on-flash data format; evaluate whether lightweight compression or reduced resolution meaningfully extends recording duration

### 4. Characterisation and validation

- Measure current consumption in each operating state: sampling, flash write burst, sleep, and BLE download
- Determine achievable recording duration for the selected configuration and compare against the analytical energy and storage budget
- Verify signal quality against reference recordings from the evaluation board
- Conduct a first practical recording — on a test subject or in the zoo cooperation, as circumstances allow — and confirm that the recovered data is usable for ODBA/VeDBA and periodicity analysis

## Research Questions

- What combination of output data rate, resolution, and duty cycle satisfies the requirements of ODBA/VeDBA and gait periodicity analysis at the lowest energy and storage cost?
- Which storage technology offers the best balance of capacity, write energy, and firmware complexity for continuous multi-day acquisition in a coin-cell-powered device?
- How much recording duration does the sensor FIFO buy, compared with per-sample MCU wake-up, and what is the measured energy saving?
- Is a primary coin cell sufficient for a useful field deployment, or does the runtime requirement force a rechargeable cell and the size penalty that comes with it?
- What buffering is required for a coin cell to sustain BLE transmission during data download without brown-out?
- Does lossless compression or reduced resolution extend recording duration enough to justify the added firmware complexity and processing energy?

## Expected Contribution

- A quantified requirements specification for animal-borne acceleration logging, derived from the analysis needs rather than assumed
- A manufactured, characterised custom PCB — schematic, layout, BOM, and assembled prototype — small and light enough for collar or harness mounting
- Firmware implementing FIFO-based low-power acquisition, flash storage, and BLE download, documented and extensible
- Measured performance data: current consumption per operating state, achievable recording duration, and validated signal quality against the existing reference
- A deployable measurement instrument for the zoo cooperation — and with it the real acceleration data that the lab's algorithm development and simulation work both depend on

This thesis is the hardware enabler for an entire research thread: the recordings it makes possible feed directly into the parallel work on activity classification and on synthetic training data generation, where real reference data is currently the limiting factor.

## Prerequisites

Solid embedded C and hands-on experience with microcontroller firmware are essential. Familiarity with PCB design (schematic capture and layout, e.g. KiCad) and an interest in low-power design are central to the work. Prior exposure to BLE and to sensor interfaces such as SPI and I²C is an advantage but can be acquired during the thesis.

Contact: markus.cremer@th-koeln.de
