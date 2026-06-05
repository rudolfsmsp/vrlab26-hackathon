// Copyright VRLab26 Hackathon. All Rights Reserved.

#include "VRLab26GameMode.h"
#include "VR/VRLab26VRCharacter.h"
#include "VR/VRLab26VRPlayerController.h"

AVRLab26GameMode::AVRLab26GameMode()
{
	DefaultPawnClass = AVRLab26VRCharacter::StaticClass();
	PlayerControllerClass = AVRLab26VRPlayerController::StaticClass();
}
