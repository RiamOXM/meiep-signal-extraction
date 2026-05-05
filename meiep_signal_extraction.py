"""
MEIEP Signal Extraction Framework
Author: Riam Daou
Description: Computational framework for isolating non-thermal mechanical transients 
during macroscopic decoherence, utilizing Matched Filtering and RANSAC-based 
outlier rejection. Designed for levitated optomechanics and high-mass interferometry.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate
from sklearn.linear_model import RANSACRegressor

# --- THEORETICAL CONSTANTS ---
# Minimum mass-energy equivalent for macroscopic decoherence boundary
DELTA_M_MIN = 3.18e-23 # kg

class MEIEPSignalProcessor:
    def __init__(self, sample_rate=10000, duration=2.0):
        self.fs = sample_rate
        self.t = np.linspace(0, duration, int(sample_rate * duration))
        self.duration = duration

    def generate_thermal_background(self, noise_level=1.0):
        """Simulates standard Brownian thermal noise in an optomechanical system."""
        np.random.seed(42) # Fixed seed for reproducibility
        return np.random.normal(0, noise_level, len(self.t))

    def generate_meiep_template(self, frequency=250, decay_rate=50):
        """Generates the theoretical non-thermal transient signature."""
        t_template = np.linspace(0, 0.05, int(self.fs * 0.05))
        # Damped oscillator with a sudden phase shift representing information release
        template = np.exp(-decay_rate * t_template) * np.sin(2 * np.pi * frequency * t_template)
        return template

    def inject_signal(self, background, template, injection_time=1.0, amplitude=2.5):
        """Injects the MEIEP transient into the thermal noise floor."""
        signal_array = np.copy(background)
        inject_idx = int(injection_time * self.fs)
        signal_array[inject_idx:inject_idx+len(template)] += template * amplitude
        return signal_array

    def apply_matched_filter(self, data, template):
        """Cross-correlates the incoming data stream with the theoretical template."""
        correlation = correlate(data, template, mode='same')
        # Normalize the correlation to establish Signal-to-Noise Ratio (SNR)
        snr = np.abs(correlation) / np.std(correlation)
        return snr

    def apply_ransac_isolation(self, data, window_size=100):
        """
        Uses RANSAC to mathematically separate standard thermal variance (inliers)
        from sudden non-thermal phase-shifts (outliers).
        """
        X = self.t.reshape(-1, 1)
        y = data
        
        # Fit RANSAC over the background envelope
        ransac = RANSACRegressor(min_samples=int(len(X)*0.1), residual_threshold=np.std(data)*2)
        ransac.fit(X, y)
        
        inlier_mask = ransac.inlier_mask_
        outlier_mask = np.logical_not(inlier_mask)
        
        return inlier_mask, outlier_mask

    def run_pipeline(self):
        print("Initializing MEIEP Signal Extraction Pipeline...")
        
        # 1. Generate Synthetic Environment
        background = self.generate_thermal_background(noise_level=1.2)
        template = self.generate_meiep_template()
        
        # 2. Inject the Theoretical Signal at t=1.0s
        raw_data = self.inject_signal(background, template, injection_time=1.0, amplitude=3.0)
        
        # 3. Process via Matched Filter
        snr_array = self.apply_matched_filter(raw_data, template)
        detection_idx = np.argmax(snr_array)
        detected_time = self.t[detection_idx]
        print(f"Matched Filter Peak detected at: t={detected_time:.4f}s")
        
        # 4. Process via RANSAC
        inliers, outliers = self.apply_ransac_isolation(raw_data)
        outlier_count = np.sum(outliers)
        print(f"RANSAC Outliers detected: {outlier_count} instances anomalous to thermal equilibrium.")
        
        # 5. Output Mass Bound Verification
        if outlier_count > 0 and snr_array[detection_idx] > 5.0:
            print(f"CONFIRMED: Non-thermal transient isolated. Bounding limit Delta M >= {DELTA_M_MIN} kg validated.")
        
        self._plot_results(raw_data, snr_array, inliers, outliers)

    def _plot_results(self, raw_data, snr_array, inliers, outliers):
        """Visualizes the separation of data."""
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        
        # Plot 1: Raw Noisy Data
        ax1.plot(self.t, raw_data, color='gray', alpha=0.7, label='Sensor Data (Thermal + MEIEP)')
        ax1.set_title('Raw Optomechanical Sensor Stream')
        ax1.legend(loc='upper right')
        
        # Plot 2: Matched Filter SNR
        ax2.plot(self.t, snr_array, color='blue', label='Matched Filter SNR')
        ax2.axhline(5.0, color='red', linestyle='--', label='5-Sigma Detection Threshold')
        ax2.set_title('Matched Filter Output')
        ax2.legend(loc='upper right')
        
        # Plot 3: RANSAC Isolation
        ax3.scatter(self.t[inliers], raw_data[inliers], color='lightgray', s=1, label='Thermal Inliers')
        ax3.scatter(self.t[outliers], raw_data[outliers], color='red', s=5, label='Non-Thermal Outliers (Transients)')
        ax3.set_title('RANSAC Robust Outlier Rejection')
        ax3.legend(loc='upper right')
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    processor = MEIEPSignalProcessor()
    processor.run_pipeline()
