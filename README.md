
# MOOSE: Measure of Optimizations On Symbolic Execution

This repository contains the source code and relevant documentation for MOOSE (Measure of Optimizations on Symbolic Execution), a comprehensive framework designed to systematically measure and analyze the impact of compiler optimizations on Dynamic Symbolic Execution (DSE) as detailed in the accompanying paper.

## Paper Abstract

Compiler optimizations often modify the performance of dynamic symbolic execution (DSE) tools, sometimes hindering and other times enhancing it. This study investigates how specific GCC and Clang compiler optimizations influence the performance of DSE techniques across a large dataset. By examining various combinations of compiler flags and their individual effects on two prominent DSE engines—angr and SymQemu—this work illuminates both positive and negative impacts and offers insights into the underlying reasons for these effects.

## Repository Contents

### Directory Structure

- `binary_generator`: Contains all source code developed for binary generator.
- `python3.8`: Contains a constomized angr. 
- `sourcefiles/`: Source files need to be tested (e.g., GCCTestsuit).

#### Requirements

- **Operating System:** Ubuntu 20.04 LTS or similar.
- **Software Requirements:**
  - GCC version 9.3.0
  - Clang version 10.0.0
  - Python 3.8 or newer
  - DSE Tools: angr, SymQemu

## Citation

If you use MOOSE in your research, please cite our paper:

```bibtex
@inproceedings{zhang2024compiler,
  title={When Compiler Optimizations Meet Symbolic Execution: An Empirical Study},
  author={Zhang, Yue and Sirlanci, Melih and Wang, Ruoyu and Lin, Zhiqiang},
  booktitle={Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security},
  year={2024},
  organization={ACM},
  address={Salt Lake City, UT, USA},
  doi={10.1145/3658644.3670372}
}
