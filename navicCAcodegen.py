## Generate CA code for NavIC 
def generateNavicCaCode(prn):
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
