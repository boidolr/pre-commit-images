pre-commit-images [![tag](https://img.shields.io/github/v/tag/boidolr/pre-commit-images?sort=semver)](https://github.com/boidolr/pre-commit-images/tags) [![Build](https://github.com/boidolr/pre-commit-images/actions/workflows/continous-integration.yml/badge.svg)](https://github.com/boidolr/pre-commit-images/actions/workflows/continous-integration.yml) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
================

Git hooks to optimize images based on the [pre-commit](https://github.com/pre-commit/pre-commit) framework. For supported image formats see the list of available hooks below.

## Using pre-commit-images with pre-commit

Add this to your `.pre-commit-config.yaml`:
```
    -   repo: https://github.com/boidolr/pre-commit-images
        rev: v1.2.2  # Use the ref you want to point at
        hooks:
        -   id: optimize-png
        # -   id: ...
```
For an extended example see [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

## Available hooks

- **`optimize-avif`**: Compress `avif` images.
    - `--threshold` can be used to configure which size difference should be used to keep the image.
    - `--qmin` to configure minimum quality setting (best: 0, worst: 63).
    - `--qmax` to configure maximum quality setting (best: 0, worst: 63).
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


## References

These hooks only work because of other projects:

- [PIL](https://github.com/python-pillow/Pillow)
- [pillow-avif-plugin](https://github.com/fdintino/pillow-avif-plugin)
- [scour](https://github.com/scour-project/scour)
