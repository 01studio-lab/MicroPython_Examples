regs = dict(
    ILI9341 = dict(
        # ili9341 registers definitions
        # LCD control registers
        NOP        = 0x00,
        SWRESET    = 0x01,    # Software Reset (page 90)
        #     LCD Read status registers
        RDDID      = 0x04,    # Read display identification 24-bit information (page 91)
        RDDST      = 0x09,    # Read Display Status 32-bit (page 92)
        RDDPM      = 0x0A,    # Read Display Power Mode 8-bit (page 94)
        RDDMADCTL  = 0x0B,    # Read Display MADCTL 8-bit (page 95)
        RDPIXFMT   = 0x0C,    # Read Display Pixel Format 8-bit (page 96)
        RDDIM      = 0x0D,    # Read Display Image Format 3-bit (page 97)
        RDDSM      = 0x0E,    # Read Display Signal Mode 8-bit (page 98)
        RDDSDR     = 0x0F,    # Read Display Self-Diagnostic Result 8-bit (page 99)
        RDID1      = 0xDA,
        RDID2      = 0xDB,
        RDID3      = 0xDC,
        RDID4      = 0xDD,
        #    LCD settings registers:
        SLPIN      = 0x10,    # Enter Sleep Mode (page 100)
        SLPOUT     = 0x11,    # Sleep Out (page 101)

        PTLON      = 0x12,    # Partial Mode ON (page 103)
        NORON      = 0x13,    # Partial Mode OFF, Normal Display mode ON

        INVOFF     = 0x20,
        INVON      = 0x21,
        GAMMASET   = 0x26,
        LCDOFF     = 0x28,
        LCDON      = 0x29,

        CASET      = 0x2A,
        PASET      = 0x2B,
        RAMWR      = 0x2C,
        RGBSET     = 0x2D,
        RAMRD      = 0x2E,

        PTLAR      = 0x30,
        MADCTL     = 0x36,
        PIXFMT     = 0x3A,    # Pixel Format Set

        IFMODE     = 0xB0,    # RGB Interface control (page 154)
        FRMCTR1    = 0xB1,    # Frame rate control (in normal mode)
        FRMCTR2    = 0xB2,    # Frame rate control (in idle mode)
        FRMCTR3    = 0xB3,    # Frame rate control (in partial mode)
        INVCTR     = 0xB4,    # Frame Inversion control (page 161)
        PRCTR      = 0xB5,    # Blanking porch control (page 162) VFP, VBP, HFP, HBP
        DFUNCTR    = 0xB6,
        ETMOD      = 0xB7,    # Entry mode set (page 168)

        PWCTR1     = 0xC0,
        PWCTR2     = 0xC1,
        PWCTR3     = 0xC2,
        PWCTR4     = 0xC3,
        PWCTR5     = 0xC4,
        VMCTR1     = 0xC5,
        VMCTR2     = 0xC7,

        GMCTRP1    = 0xE0,
        GMCTRN1    = 0xE1,
        #PWCTR6     =  0xFC,
        IFCTL      = 0xF6,
        )
)
