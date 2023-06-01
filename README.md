# Cell Counter

Count cells on a hemocytometer plate. Developed for use at the Bebout Lab, NASA Ames.

## Running

To use, simply upload your selected files and set your classification parameters. 
* CLI: `pip install -r requirements.txt`, then `python cell-cli.py`
* (No longer hosted) ~~Website: https://rapid-cell-counter.herokuapp.com/~~

## Example
Before:
![Before](https://cloud.githubusercontent.com/assets/1396242/16716266/1f135a34-46ac-11e6-8c64-5cc7661f832e.jpg)

After:
![After](https://cloud.githubusercontent.com/assets/1396242/16716264/1a70bc56-46ac-11e6-8d9d-92eec5fda6d9.png)

## Acknowledgements

This site uses the [TrackPy - Particle Tracking Toolkit](https://github.com/soft-matter/trackpy). 

## Future plans

The next version of this site will use a least squares approach to iteratively determining the best fit parameters.
