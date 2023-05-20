#!/usr/bin/python3

import argparse
import os
import glob
import itertools

import shutil


HOME = os.path.expanduser("~")
SSH_PATH = os.path.join(HOME, ".ssh")
ID_RSA = os.path.join(SSH_PATH, "id_rsa")
ID_RSA_PUB = os.path.join(SSH_PATH, "id_rsa.pub")
KNOWN_HOSTS = os.path.join(SSH_PATH, "known_hosts")
CURRENT_PROFILE = os.path.join(SSH_PATH, "current")


def get_args():
    parser = argparse.ArgumentParser(
        "ssh-switch", description="switches system ssh profiles"
    )
    parser.add_argument("profile", help="profile alias to switch", nargs="?")
    parser.add_argument(
        "--create",
        help="creates profile based on current system id_rsa and id_rsa.pub and switches to it",
        action="store_true",
    )
    parser.add_argument(
        "--current",
        help="prints current profile",
        action="store_true",
    )

    parser.add_argument(
        "--list",
        help="prints list of profiles",
        action="store_true",
    )

    return parser.parse_args()


def get_profiles():
    files = glob.glob(os.path.join(SSH_PATH, "*"))
    current_profile = get_current_profile()
    current_profile_path = os.path.join(SSH_PATH, current_profile)
    profiles = (
        os.path.split(file)[-1]
        for file in files
        if os.path.isdir(file) and file != current_profile_path
    )
    profiles = itertools.chain([f"*{current_profile}"], profiles)
    print("\n".join(profiles))


def get_current_profile():
    if not os.path.exists(CURRENT_PROFILE):
        print("You need one created profile at least")
        print("Use --create")
        exit(1)
    with open(CURRENT_PROFILE) as file:
        return file.read()


def set_current_profile(profile):
    with open(CURRENT_PROFILE, "w") as file:
        file.write(profile)


def get_profile_path(profile):
    return os.path.join(SSH_PATH, profile)


def create(profile):
    profile_path = get_profile_path(profile)
    if os.path.exists(profile_path):
        print("Profile already exists")
        exit(1)
    if not os.path.exists(ID_RSA) or not os.path.exists(ID_RSA_PUB):
        print("RSA files don't exist. Generate them via ssh-keygen")
        exit(1)

    os.makedirs(profile_path)
    for file in ID_RSA, ID_RSA_PUB:
        shutil.copy(file, profile_path)
    with open(os.path.join(profile_path, "known_hosts"), "w"):
        pass
    if not os.path.exists(CURRENT_PROFILE):
        set_current_profile(profile)
    switch(profile)


def switch(profile):
    profile_path = get_profile_path(profile)
    if not os.path.exists(profile_path):
        print("Profile doesn't exist")
        exit(1)

    current_profile = get_current_profile()
    shutil.copy(KNOWN_HOSTS, get_profile_path(current_profile))
    shutil.copy(os.path.join(profile_path, "id_rsa"), ID_RSA)
    shutil.copy(os.path.join(profile_path, "id_rsa.pub"), ID_RSA_PUB)
    shutil.copy(os.path.join(profile_path, "known_hosts"), KNOWN_HOSTS)
    set_current_profile(profile)


def main():
    args = get_args()

    os.makedirs(SSH_PATH, exist_ok=True)

    if args.create:
        create(args.profile)
    elif args.current:
        print(get_current_profile())
    elif args.list:
        get_profiles()
    else:
        switch(args.profile)


if __name__ == "__main__":
    main()
