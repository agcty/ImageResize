import os
import argparse

# Parse Arguments
parser = argparse.ArgumentParser(description='Resize images and compress them')

parser.add_argument("-s", dest="size", help="Define the new size of the picture, default 2048x2048", default="2048x2048",
                    type=str)
parser.add_argument("-q", dest="quality", help="define the compressed quality, default 90", default="90",
                    type=str)
parser.add_argument("-overwrite", dest="overwrite", type=bool,
                    help="flag for overwriting source files, default true", default=True)
args = parser.parse_args()

print("Options: Size %s, Quality %s" % (args.size, args.quality))
# Which directory do you want to start with?
working_dir = os.getcwd()
target = working_dir + "/Bearbeitet/"

# create target directory for non-destructive operation
try:
    os.mkdir(target)
except OSError:
    print("Creation of the directory %s failed" % target)
else:
    print("Successfully created the directory %s " % target)


def resize_images_safely(directory):
    # define location to save image
    save_to = target + os.path.basename(os.path.normpath(directory))
    print("Saving location: %s" % save_to)

    # create saving location
    try:
        os.mkdir(save_to)
    except OSError:
        print("Creation of the directory %s failed" % save_to)
    else:
        print("Successfully created the directory %s " % save_to)

    # define command for resizing
    command = "mogrify \
    -shave 5x5 \
    -background white \
    -gravity center   \
    -resize {} -extent {} \
    -interlace Plane \
    -gaussian-blur 0.05 \
    -quality {}% \
    -path {} \
    -format jpg *.jpg;".format(args.size, args.size, args.quality, '"' + save_to + '"')

    print("Resizing (overwrite) in: %s" % directory)
    # execeute command
    os.system(command)


def resize_images_overwrite(directory):
    # define command for resizing
    command = "mogrify \
    -shave 5x5 \
    -gravity center   \
    -resize {} -extent {} \
    -interlace Plane \
    -quality {}% \
    -format jpg *.*;".format(args.size, args.size, args.quality)

    print("Resizing in: %s" % directory)
    # execeute command
    os.system(command)


# Get all the subdirectories of working_dir recursively and store them in a list:
directories = [os.path.abspath(x[0]) for x in os.walk(working_dir)]

# iterate over directories and run resize
for directory in directories:
    # Change working Directory
    os.chdir(directory)
    print("Changing directory: %s" % directory)
    # Run your function
    if (args.overwrite):
        resize_images_overwrite(directory)
    else:
        resize_images_safely(directories)