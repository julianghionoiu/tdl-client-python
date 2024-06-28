#!/bin/bash

SCRIPT_FOLDER="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION_FILE="${SCRIPT_FOLDER}/previous_version.py"

echo "Reading setup.py properties. This might take some time."

# Previous
PREVIOUS_VERSION=$(python previous_version.py)
echo "PREVIOUS_VERSION = $PREVIOUS_VERSION"
CURRENT_VERSION=$(python setup.py --version)
echo "CURRENT_VERSION = $CURRENT_VERSION"

# Prompt for version confirmation
read -p "Going to release version ${CURRENT_VERSION} (previous ${PREVIOUS_VERSION}). Proceed ? [y/n] "
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Aborting."
    exit
fi

# Release current version
git tag -a "v${CURRENT_VERSION}" -m "Release ${CURRENT_VERSION}"
git push origin "v${CURRENT_VERSION}"
echo "Pushed tag to Git origin. It will now trigger the deployment pipeline."

cat > "${VERSION_FILE}" <<-EOF
from __future__ import print_function

PREVIOUS_VERSION = '$CURRENT_VERSION'


def main():
    print(PREVIOUS_VERSION)


if __name__ == "__main__":
    main()

EOF