# SH_Flow
Repo for generating SH signals with conditional flows

Context parameters: The masses of the unkown particles mX, mS

Distribution to generate: Conditional NN ouptut as a function of mX, mS. 

Expected behaviour: Signals peak at 1 (i.e. signal like) only if true mX, mS = target mX, mS. Else they peak at 0 (background like). 

## Preprocess

Convert your root files to a pandas dataframe and store it in data.parquet.

```python process_data.py```

## Training

