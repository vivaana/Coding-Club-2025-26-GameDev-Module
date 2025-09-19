import cx_Freeze
executables = [cx_Freeze.Executable("AlienShooter.py")]

cx_Freeze.setup(
    name = "Alien Shooter",
    options={"build_exe": {"packages": ["pygame"], "include_files":["alien.png","bullet.png","heart.png","player.png","PlayerUpgrade.png","shield.png","SpaceQuest-Xj4o.ttf","uncollectibleBullet.png","uncollectibleHeart.png","UncollectibleUpgrade.png","uncShield.png"]}},
    executables = executables
)