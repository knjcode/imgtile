# imgtile

A script to tile images.

# Samples

## Tile 100 faces

```
$ ./imgtile.py 100faces --size 16x16
```

![Tile 100 faces](samples/sample.png)

## Tile 8 faces with 3px gray spaces

```
$ ./imgtile.py 100faces --size 32x32 --limit 8 --space 3 --space-color gray
```

![Tile 8 faces with 3px gray spaces](samples/sample2.png)

## Tile 8 faces by 6 units with 2px spaces

```
$ ./imgtile.py 100faces --size 32x32 --limit 8 --space 2 --tile-num 6
```

![Tile 8 faces by 6 units with 2px spaces](samples/sample3.png)

These sample images are taken from [Labeled Faces in the Wild dataset](http://vis-www.cs.umass.edu/lfw/).

# Setup

```
$ git clone https://github.com/knjcode/imgtile.git
$ cd imgtile
$ pip install -r requirements.txt
```

# Simple usage

Put images in a directory. Run this tool with directory name.

```
$ ./imgtile.py target_dir
```

Then, open output.png

# Options

- Specify output filename

  `--output` (default 'output.png')

  ```
  $ ./imgtile.py target_dir --output result.jpg
  ```

- Create images per subdirectory of target directory

  `--per-subdir`

  ```
  $ ./imgtile.py target_dir --per-subdir
  ```

- Resize images

  `--size` (default '128x128')

  ```
  $ ./imgtile.py target_dir --size 64x64
  ```

- Keep aspect ratio (Not implemented yet)

  `--keep-aspect` (default 'False')

  ```
  $ ./imgtile.py target_dir --keep-aspect
  ```

- Set space between images

  `--space` (default 0px)

  ```
  $ ./imgtile.py target_dir --space 5
  ```

- Set space color between images

  `--space-color` (default 'black')

  Specify a color by name (gray, for example)
  ```
  $ ./imgtile.py target_dir --space 5 --space-color gray
  ```

  Specify a color by three integer values between 0 and 255 without spaces (gray is 128,128,128, for example)
  ```
  $ ./imgtile.py target_dir --space 5 --space-color 128,128,128
  ```

- Specify horizontal tile number

  `--tile-num`

  ```
  $ ./imgtile.py target_dir --tile-num 64
  ```

- Limit the number of tiling images

  `--limit`

  ```
  $ ./imgtile.py target_dir --limit 100
  ```

- Display result image for iTerm2 (like a imgcat)

  `--imgcat`

  ```
  $ ./imgtile.py target_dir --imgcat
  ```

- Display progress bar while loading

  `--progress`

  ```
  $ ./imgtile.py target_dir --progress
  ```

## License

MIT
