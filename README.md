# Navic-receiver-module-on-rtlsdr

## Description
This project is the implementation of Standalone RX module for NavIC (IRNSS) systems operating on L5 Band (1176.45 MHz)

## Requirements:
- RTL SDR dongle
- GNU Radio
- Python :
	- Numpy
	- Matplotlib (For displaying the graphs)

## Project Files Organisation:

*Currently all the implementations of acquisition, tracking & post processing are done on python, but i am porting them into C implementation for higher efficiency.*

1. RF front end implementation is done using GNU radio `Navic_RF_signal_Acquisition_Block_using_RTLSDR.grc`:
   - It tunes RTL-SDR for L5 Band (1176.45 MHz) and grabs the IQ data & Store it in file (I did store them on ram disk).
2. The NavIC system PRN C/A code generation is implemented as modules in `navicCAcodegen.py` which are imported for acquisition and tracking blocks.
3. Acquisition & Tracking Blocks are implemented in `navic_receiver_block.ipynb` :
   - It takes the stored IQ data file and go through Acquisition and then to Tracking of the SAT using CA codes generation modules from `navicCAcodegen.py` and then store the final tracking results to `trackResults.npy`
4. The Post Processing of Tracking results are done using `navic_postProcessing_block.ipynb`:
   - It demodulates the Navigation Bits and do the Preamble detection and thereby extracts the subframes.
   - Finally It extracts the Navigation Data viz : TOW and Ephemeris data.
5. The `PROJECT_REPORT.pdf` contains all the Implementation Details along with the system working description/internals. It is the documentation of this project.

