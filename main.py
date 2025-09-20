import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers.registration_controller import RegistrationController

def main():
    print("Starting Student Registration System...")
    controller = RegistrationController()
    controller.run()

if __name__ == "__main__":
    main()
