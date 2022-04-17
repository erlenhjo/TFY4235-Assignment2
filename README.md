# Assignment-2
 Second assignment for NTNU course TFY4235 Numerical Physics spring 2022.

## Project files







## Project progress
### Basic euler scheme requirements
- [x] Implement potential and force
- [x] Implement gaussian PRNG
- [x] Check gaussian PRNG
- [x] Implement Euler scheme
- [x] Calculate timestep
- [x] Implement basic input/output

### Data storage routines
- [x] Determine folder structure
- [x] Store trajectories
- [ ] Store end points
- [x] Store metadata 
- [x] Access trajectories
- [ ] Access end points
- [x] Access metadata

### Particle simulations - Constant potential
- [ ] Run with constant potential for different deltaU
	- [ ] Determine N and number of particles in parallell	
- [ ] Compare position distribution with Boltzmann distribution
	- [ ] Plot of trajectories
	- [ ] Occupied/visited? potential energy vs Boltzmann
- [x] Check that Boltzmann distribution is well normalized
- [ ] Determine deltaU for drift to the right with flashing
- [ ] Predict 3 regimes of drift efficiency

### Particle simulations - Flashing potential
- [ ] Run with 80 eV flashing potential for different tau
	- [ ] Determine tau values
	- [ ] Determine N and number of particles in parallell
- [ ] Plot trajectries for different tau
	- [ ] One for each drift efficiency regime
- [ ] Calculate average drift velocity as function of tau
- [ ] Estimate optimal tau for max drift velocity
- [ ] Compare with literature
- [ ] Compare with larger particle
	- [ ] Show that it is equivalent to a change of timescale in reduced units
	- [ ] Deduce avg. drift velocity as a function of tau
	- [ ] Predict drift velocity at optimal tau for the smaller particle
	- [ ] Rerun with larger particle at optimal tau and compare

### Visualisation of particle density
- [ ] Implement no potential euler scheme in normal units
- [ ] Run no potential simulation
- [ ] Visualize motion of ensemble and particle density as a function of time
	- [ ] For no potential
	- [ ] Compare no potential to diffusion equation up to statistical noise
	- [ ] For flashing potential for both particles at optimal tau
	- [ ] Describe time evolution with a PDE

	
