## Generate CA code for NavIC 
import numpy as np

codeFreqBasis = 1023000.0
codeLength = 1023


def genNavicCaCode(prn):
    """
    Takes PRN (ie Satellite ID - 1 ) as Input  and outputs CA code sequece (chips) of 1023 length.
    In Output : -1 refers to '0' Binary state and +1 refers to '1' Binary state in Polar NRZ format
    """
    #prn = SATID - 1
    g2s = [448, 603, 442, 758, 690, 
           917, 830, 600, 601, 377,
           602, 866, 877, 351 ]
    g2shift = g2s[prn]
    
    # Generate G1 code
    g1 = np.zeros(1023,np.int8)
    reg = -1 * np.ones(10,np.int8)
    for i in range(1023):
            g1[i] = reg[-1]
            saveBit = reg[2] * reg[9]
            reg[1:] = reg[:-1]
            reg[0] = saveBit
    # Generate G2 code
    g2 = np.zeros(1023,np.int8)
    reg = -1 * np.ones(10,np.int8)
    for i in range(1023):
        g2[i] = reg[-1]
        saveBit = reg[1] * reg[2] * reg[5] * \
                  reg[7] * reg[8] * reg[9]
        reg[1:] = reg[:-1]
        reg[0] = saveBit
        
    ## Applying shifting to g2 code
    g2 = np.r_[g2[1023-g2shift:],g2[:1023-g2shift]]

    ## Generate CA code using mod2 mul
    CAcode = -g1 * g2
    
    return CAcode

def genNavicCaTable(samplingFreq):
    """
    Takes Sampling Frequecy as input.
    Return CA code table of Navic giving all 14 PRN codes.
    """
    ## make CA table corresponding to the sampling frequecy
    samplesPerCode = np.long(np.round(samplingFreq / (codeFreqBasis / codeLength)))
    caCodesTable = np.zeros((32, samplesPerCode),np.int8)
    # --- Find time periods --------------------------------------------------
    tsamp = 1.0 / samplingFreq

    tcode = 1.0 / codeFreqBasis

    # === For all satellite PRN-s ...
    for PRN in range(14):
        # --- Generate CA code for given PRN -----------------------------------
        caCode = genNavicCaCode(PRN)

        # --- Make index array to read C/A code values -------------------------
        # The length of the index array depends on the sampling frequency -
        # number of samples per millisecond (because one C/A code period is one
        # millisecond).
        codeValueIndex = np.ceil( (tsamp/tcode) * np.arange(1, samplesPerCode + 1) ) - 1
        codeValueIndex = np.int16(codeValueIndex)

        codeValueIndex[-1] = 1022

        # The "upsampled" code is made by selecting values form the CA code
        # chip array (caCode) for the time instances of each sample.
        caCodesTable[PRN] = caCode[codeValueIndex]
    return caCodesTable

