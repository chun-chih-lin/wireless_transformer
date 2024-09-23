### 1. We collected the dataset in a real environment; hence, you can only calculate the SNR for each data sample. I also labeled data samples with different transmission power in dBm.
I updated the shared Google Drive, and it contains 6 files with ambient noise. You need to calculate the SNR by those samples. 

**For sample**  
For file names "Dataset_EIB_3F_Hallway_0430_SR20_CF2360_I0.pkl"  
It received the ambient noise in the "EIB_3F_Hallway_0430" location, with a sampling rate at 20 MHz, on the 2360 MHz frequency band and without any injected interference.

### 2. The Label is listed below
- Label - 0: WiFi-BPSK  
- Label - 1: WiFi-QPSK  
- Label - 2: WiFi-16QAM  
- Label - 3: WiFi-64QAM  
- Label - 4: ZigBee-OQPSK  
- Label - 5: BT-LE1M  
- Label - 6: BT-LE2M  
- Label - 7: BT-S2  
- Label - 8: BT-S8  
- Label - 9: Pure Noise  

### 3. The file info is described below

```
Dataset_EIB_Outdoor_TP{transmission power in dbm}_D{distance between TX and RX}_SR{sampling rate at RX}_CF{Centering Frequency in MHz}_I{w/ w/o interference flag}
```

**Dataset_EIB_Outdoor_TP5_D5_SR20_CF2360_I1**  
- Transmission power at 5 dBm.  
- The distance between TX and RX is 5 meters.  
- The RX's receiving sampling rate is 20 MHz.  
- The collection is done at the 2360MHz frequency band.  
- This dataset is done with another fixed interference source.  

---
Please let me know if you have any questions.
**chunchi@clemson.edu**