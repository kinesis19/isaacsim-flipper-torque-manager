# import necessary modules
import omni.usd
from pxr import Usd, UsdGeom, UsdPhysics

# Attempt to get the current stage
try:
    STAGE = omni.usd.get_context().get_stage()
except Exception as e:
    STAGE = None
    print(f"Error getting stage: {e}")


# Function to set the mass of a prim
def set_prim_mass(prim_path: str, mass_kg: float):
    if STAGE is None:
        print("No valid stage found.")
        return

    prim = STAGE.GetPrimAtPath(prim_path)
    if not prim.IsValid():
        print(f"Prim at path '{prim_path}' does not exist.")
        return

    try:
        mass_api = UsdPhysics.MassAPI.Apply(prim)
        mass_attr = mass_api.GetMassAttr()
        
        if not mass_attr:
            mass_attr = mass_api.CreateMassAttr()
            print(f"Created mass attribute for {prim_path}")

        mass_attr.Set(mass_kg)
        print(f"Mass for '{prim_path}' set to: {mass_kg} kg")
    
    except Exception as e:
        print(f"Error setting mass for '{prim_path}': {e}")
        import traceback
        traceback.print_exc()

# Function to set up robot masses
def setup_robot_masses():
    print("Setting up robot masses")

    robot_parts = {
        "/World/cygnus/base_link": 50.0, # kg
        "/World/cygnus/flipper_back_left_1": 6.0, # kg
        "/World/cygnus/flipper_back_right_1": 6.0, # kg
        "/World/cygnus/flipper_front_left_1": 6.0, # kg
        "/World/cygnus/flipper_front_right_1": 6.0, # kg
    }

    if STAGE is None:
        print("No valid stage found. Cannot set up robot masses.")
        return
    
    for prim_path, mass in robot_parts.items():
        set_prim_mass(prim_path, mass)

    print("Robot masses setup complete.")


# System
if STAGE is None:
    print("No valid stage found. Exiting setup.")
else:
    try:
        setup_robot_masses()
    except Exception as e:
        print(f"Error during setup: {e}")
        import traceback
        traceback.print_exc()

# if __name__ == "__main__":
#     if STAGE is None:
#         print("No valid stage found. Exiting setup.")

#     else:
#         try:
#             setup_robot_masses()
#         except Exception as e:
#             print(f"Error during setup: {e}")
#             import traceback
#             traceback.print_exc()
