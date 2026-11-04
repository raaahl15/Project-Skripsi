# README Dryad — Essig et al. (doi:10.5061/dryad.ht76hdrk7)

> Salinan README asli dari Dryad (diunduh pengguna 4 Nov 2026), disimpan apa adanya di bawah garis.
> **Catatan kita:** README ini tidak memuat nama penanda per kanal. Urutan kanal diambil dari notebook resmi
> penulis, lihat bagian "Urutan kanal" di bawah dan `docs/DATASET-KANDIDAT.md` §1.

## Urutan kanal (sumber: notebook penulis, bukan README)
Sumber: `marrlab/scifAI-notebooks`, file `0 - Feature extraction/Data exploration.ipynb`, sel ke-20 (dikutip apa adanya):

```python
channel_names = {
         "Ch1": "BF",
         "Ch2": "Antibody",
         "Ch3": "CD18",
         "Ch4": "F-Actin",
         "Ch5": "MHCII",
         "Ch6": "CD3",
         "Ch7": "P-CD3zeta",
         "Ch8": "Live-Dead"}
```

Ch1–Ch8 dipetakan ke indeks 0–7 pada array `image[..., c]`. Kanal 0 = brightfield sudah dicek secara visual.
Pemetaan ini masih asumsi: notebook tidak menunjukkan bagaimana nama "ChN" dibuat dari array h5.

---

# Imaging flow cytometry dataset for profiling the immunological synapse of therapeutic antibodies
---

This data repository contains imaging flow cytometry (IFC) data of immunological synapse of T-B conjugates. The dataset includes T cells from nine donors in four different experiments. In addition, it includes different antigens and three antibodies: CD19-TCB, CD20-TCB and Teplizumab

## Data structure
Each image is saved as a `.h5` file. It includes these keys: `image`, `mask`. In case there is a label available, the `label` is provided as `str`. The image is a 16-bit image with one bright field channel and multiple fluorescent channels. The mask is the corresponding segmentation for each channel.
Additionally, each file name includes a number, which is the object number from the IFC experiments. Apart from each file, the data comes from four experiments, nine donors, and these conditions: -SEA, +SEA, Teplizumab, CD19-TCB, and CD20-TCB.

This is the complete set of donors and experiments. In addition, you can find more info in the supplementary figures about the age and gender of each donors.

```bash
data_path/Experiment_1/Donor_1/{-SEA,+SEA,Isotype,Teplizumab}/*.h5
data_path/Experiment_1/Donor_2/{-SEA,+SEA,Isotype,Teplizumab}/*.h5
data_path/Experiment_2/Donor_3/{-SEA,+SEA,Isotype,Teplizumab}/*.h5
data_path/Experiment_2/Donor_4/{-SEA,+SEA,Isotype,Teplizumab}/*.h5
data_path/Experiment_3/Donor_1/{-SEA,+SEA,Isotype,Teplizumab,DIG-TCB,CD19-TCB,CD20-TCB}/*.h5
data_path/Experiment_3/Donor_5/{-SEA,+SEA,Isotype,Teplizumab,DIG-TCB,CD19-TCB,CD20-TCB}/*.h5
data_path/Experiment_3/Donor_6/{-SEA,+SEA,Isotype,Teplizumab}/*.h5
data_path/Experiment_4/Donor_2/{-SEA,+SEA,DIG-TCB,CD19-TCB,CD20-TCB}/*.h5
data_path/Experiment_4/Donor_7/{-SEA,+SEA,DIG-TCB,CD19-TCB,CD20-TCB}/*.h5
data_path/Experiment_4/Donor_8/{-SEA,+SEA,DIG-TCB,CD19-TCB,CD20-TCB}/*.h5
data_path/Experiment_4/Donor_9/{-SEA,+SEA,DIG-TCB,CD19-TCB,CD20-TCB}/*.h5
```
(Daftar folder diringkas dengan kurung kurawal; README asli menulisnya satu per baris dan mencantumkan Experiment_3/Donor_1 dua kali.)

## How to use the data
For using the datasets, you need to download and unpack the files. However, please be aware that you would need nearly a Terabyte space to unpack the data.

After that, you can simply use the scifAI package: https://github.com/marrlab/scifAI

## How to use the data with scifAI
```python
import scifAI
metadata = scifAI.metadata_generator(data_path)

from sklearn.pipeline import FeatureUnion, Pipeline
from scifAI.ml import features, FeatureExtractor
feature_union = FeatureUnion([
    ("MaskBasedFeatures", features.MaskBasedFeatures()),
    ("GLCMFeatures", features.GLCMFeatures()),
    ("GradientRMS", features.GradientRMS()),
    ("BackgroundMean", features.BackgroundMean()),
    ("PercentileFeatures", features.PercentileFeatures()),
    ("CellShape", features.CellShape()),
    ("Collocalization", features.Collocalization()),
    ("IntersectionProperties", features.IntersectionProperties()),
    ("CenterOfCellsDistances", features.CenterOfCellsDistances())])
pipeline = Pipeline([("features", feature_union)])
list_of_features = FeatureExtractor(pipeline).extract_features(metadata)
df_features = pd.DataFrame(list_of_features)
```
Considering that there are many features, we suggest reducing the features with no variance. In addition, imputing with `0.` is the best option as it follows the biological assumptions for the feature extraction process.
```python
df_features = df_features.fillna(0.)
df_features = df_features.loc[:, df_features.std() > 0.]
```
