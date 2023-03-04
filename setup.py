from setuptools import setup
setup(
  name = 'landmark_registration',
  packages = ['landmark_registration'],
  version = '1.0',
  description = 'Given the pixel coordinates of multiple landmarks, can their locations (and the locations of the cameras) be inferred.',
  author = 'Mike Smith',
  author_email = 'm.t.smith@sheffield.ac.uk',
  url = 'https://github.com/lionfish0/landmark_registration.git',
  download_url = 'https://github.com/lionfish0/landmark_registration.git',
  keywords = ['registration','3d','landmarks','cameras','images','align'],
  classifiers = [],
  install_requires=['numpy'],
)
