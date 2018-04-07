# Pandas structures

## Series

### Initializing

*Series**

```python

# Series(data=None, index=None, dtype=None, name=None, copy=False, fastpath=False)

# from a list
s1 = pd.series([1, 2, 3]) 

# from a list with indexes
s2 = pd.series([1, 2, 3], index = ['a', 'b', 'c']) 

# from a dictionary
s3 = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000} 
```

`s.values` returns a numpy array object with the values of the series. 
`s.index` returns a index object. It can be a range index object or a base index object depeding on the type of range used for the series. Index values can be used to select elements from the series (e.g. `s['b']`).
`s.name` and `s.index.name`return the names of the series and of the index object.

**DataFrame**

```python
# DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)

# from a dictionary of lists
d = {'ID' : [1, 2, 3], 'Name' : ['Al', 'Bae', 'Cid'], 'Age' : [2, 41, 25]}
s1 = DataFrame(d) 

# from a dictionary with columns
s2 = DataFrame(d, columns = ['Name', 'ID', 'Age', 'Surname']) # Columns not in the dict will be NaN

# from a dictionary with an index
s3 = DataFrame(d, index = ['a', 'b', 'c'])

# from a nested dict
pop = {'Nevada': {2001: 2.4, 2002: 2.9}, 'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}} # the oouter keys are columns, the inner keys are rows

```
`s.values` returns a 2D numpy array object with the values of the series. 
`s.columns` returns an index object with the df columns. The column returned when indexing a DataFrame is a view on the underlying data, not a copy.


**Index objects**

Index object are immutable, and cannot be modified. An Index also functions as a fixed-size set.

| Method | Description |
| ------ | ----------- |
| append | Concatenate with additional Index objects, producing a new Index |
| diff | Compute set difference as an Index |
| intersection | Compute set intersection | 
| union | Compute set union |
| isin | Compute boolean array indicating whether each value is contained in the passed collection |
| delete | Compute new Index with element at index i deleted |
| drop | Compute new index by deleting passed values | 
| insert | Compute new Index by inserting element at index i | 
| is_monotonic | Returns True if each element is greater than or equal to the previous element | 
| is_unique | Returns True if the Index has no duplicate values | 
| unique | Compute the array of unique values in the Index |

### Selecting the data

Dataframe columns can be selected either by dict-like notation, `s['col']`, or as an attribute, `s.col`.

`del s.col_name` will delete a df column

`s.T` will transpose the df





















