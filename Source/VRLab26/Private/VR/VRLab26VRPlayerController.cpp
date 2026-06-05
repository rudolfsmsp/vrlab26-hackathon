// Copyright VRLab26 Hackathon. All Rights Reserved.

#include "VR/VRLab26VRPlayerController.h"

#include "HeadMountedDisplayFunctionLibrary.h"

AVRLab26VRPlayerController::AVRLab26VRPlayerController()
{
	bShowMouseCursor = false;
}

void AVRLab26VRPlayerController::BeginPlay()
{
	Super::BeginPlay();

	UHeadMountedDisplayFunctionLibrary::EnableHMD(true);
}
