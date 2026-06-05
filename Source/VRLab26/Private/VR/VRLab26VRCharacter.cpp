// Copyright VRLab26 Hackathon. All Rights Reserved.

#include "VR/VRLab26VRCharacter.h"

#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "MotionControllerComponent.h"

namespace VRLab26OpenXRSources
{
	const FName LeftGrip(TEXT("LeftGrip"));
	const FName RightGrip(TEXT("RightGrip"));
	const FName LeftAim(TEXT("LeftAim"));
	const FName RightAim(TEXT("RightAim"));
}

AVRLab26VRCharacter::AVRLab26VRCharacter()
{
	PrimaryActorTick.bCanEverTick = false;

	GetCapsuleComponent()->InitCapsuleSize(42.f, 96.f);
	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = true;
	bUseControllerRotationRoll = false;

	VRCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("VRCamera"));
	VRCamera->SetupAttachment(GetCapsuleComponent());
	VRCamera->SetRelativeLocation(FVector(0.f, 0.f, 64.f));
	VRCamera->bUsePawnControlRotation = false;

	LeftGripController = CreateDefaultSubobject<UMotionControllerComponent>(TEXT("LeftGripController"));
	LeftGripController->SetupAttachment(VRCamera);

	RightGripController = CreateDefaultSubobject<UMotionControllerComponent>(TEXT("RightGripController"));
	RightGripController->SetupAttachment(VRCamera);

	LeftAimController = CreateDefaultSubobject<UMotionControllerComponent>(TEXT("LeftAimController"));
	LeftAimController->SetupAttachment(VRCamera);

	RightAimController = CreateDefaultSubobject<UMotionControllerComponent>(TEXT("RightAimController"));
	RightAimController->SetupAttachment(VRCamera);
}

void AVRLab26VRCharacter::ConfigureMotionController(UMotionControllerComponent* Component, FName MotionSource) const
{
	if (!Component)
	{
		return;
	}

	Component->SetTrackingMotionSource(MotionSource);
	Component->bDisplayDeviceModel = true;
}

void AVRLab26VRCharacter::BeginPlay()
{
	Super::BeginPlay();

	using namespace VRLab26OpenXRSources;
	ConfigureMotionController(LeftGripController, LeftGrip);
	ConfigureMotionController(RightGripController, RightGrip);
	ConfigureMotionController(LeftAimController, LeftAim);
	ConfigureMotionController(RightAimController, RightAim);
}
