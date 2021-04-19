[![Testing](https://github.com/adamurban98/cubemem/actions/workflows/test.yml/badge.svg)](https://github.com/adamurban98/cubemem/actions/workflows/test.yml)

# Cubemem 

Try it here: [cubemem.adamurban.net 🌍](https://cubemem.adamurban.net/)

## Todo
- [x] shuffle records moves
- [x] default preferences
- [ ] allow (again) text based input and gracefull fail on cubecodes with mistakes
- [x] warn on misalligned cubes
- [x] suggest setup moves
- [ ] alternative algorithms for edge solution
- [x] write howto
- [ ] allow to choose buffer stickers and swap algorithms
- [ ] rotate the sticker label in 3d view on the top and bottom cube face
- [ ] normalize cube codes (rare)

## Bugs

- When preference for 2d cube is set in the guide, the 3d cube does not respect the "always" option for sticker labels.

## Testing
- To test: `pytest`
- To see coverage: `coverage run --omit='test_*.py' -m  pytest && coverage report`