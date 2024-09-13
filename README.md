pre-commit-images
[![tag](https://img.shields.io/github/v/tag/boidolr/pre-commit-images?sort=semver)](https://github.com/boidolr/pre-commit-images/tags)
![python](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fboidolr%2Fpre-commit-images%2Fmain%2Fpyproject.toml)
[![Build](https://github.com/boidolr/pre-commit-images/actions/workflows/continous-integration.yml/badge.svg)](https://github.com/boidolr/pre-commit-images/actions/workflows/continous-integration.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
================

Scripts that can work as `git` hooks to optimize and manipulate images.
These scripts can be called directly or with the provided configration for the [pre-commit](https://github.com/pre-commit/pre-commit) framework.
For details see below.


## Using pre-commit-images with pre-commit

Add this to your `.pre-commit-config.yaml`:
```
    -   repo: https://github.com/boidolr/pre-commit-images
        rev: v1.8.1  # Use the ref you want to point at
        hooks:
        -   id: optimize-png
        # -   id: ...
```
For an extended example see [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

### Available hooks

- **`optimize-avif`**: Compress `avif` images.
    - `--threshold` can be used to configure which size difference should be used to keep the image.
    - `--quality` to configure minimum quality setting (best: 100, worst: 0).
    - `--effort` to set the quality/speed tradeoff (slowest: 0, fastest: 10).
- **`optimize-jpg`**: Compress `jpeg` images.
    - `--threshold` can be used to configure which size difference should be used to keep the image.
    - `--quality` can be used to configure quality setting for a JPG image.
- **`optimize-png`**: Compress `png` images.
    - `--threshold` can be used to configure which size difference should be used to keep the image.
- **`optimize-svg`**: Compress `svg` images.
    - `--threshold` can be used to configure which size difference should be used to keep the image.
- **`optimize-webp`**: Compress `webp` images.
    - `--threshold` can be used to configure which size difference should be used to keep the image.
    - `--lossless` switch to lossless compression.
    - `--quality` can be used to configure quality setting for lossy compression or effort to spend on lossless compression.
- **`resize`** (experimental): Resize `avif`, `jpeg`, `png` and `webp` images with fixed dimensions. Required options:
    - `--width` new width of images.
    - `--height` new height of images.


## Using scripts directly

Install the package to get access to the scripts defined as command line entry points in [`pyproject.toml`](./pyproject.toml).
The scripts accept the arguments given for the pre-commit hooks. Additionally they exepect to receive the file names to work on.

An example invocation could be `uvx --from 'git+https://github.com/boidolr/pre-commit-images.git[avif]' optimize-avif tests/test.avif`.

Available entry points are identical to the pre-commit hooks:
- `optimize-avif`
- `optimize-jpg`
- `optimize-png`
- `optimize-svg`
- `optimize-webp`
- `resize`


## References

These hooks only work because of other projects:

- [PIL](https://github.com/python-pillow/Pillow)
- [pillow-avif-plugin](https://github.com/fdintino/pillow-avif-plugin)
- [scour](https://github.com/scour-project/scour)
