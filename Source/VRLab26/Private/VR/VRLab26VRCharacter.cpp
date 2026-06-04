// Copyright VRLab26 Hackathon. All Rights Reserved.

#include "VR/VRLab26VRCharacter.h"

#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "MotionControllerComponent.h"

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

	LeftMotionController = CreateDefaultSubobject<UMotionControllerComponent>(TEXT("LeftMotionController"));
	LeftMotionController->SetupAttachment(VRCamera);
	LeftMotionController->SetTrackingSource(EControllerHand::Left);

	RightMotionController = CreateDefaultSubobject<UMotionControllerComponent>(TEXT("RightMotionController"));
	RightMotionController->SetupAttachment(VRCamera);
	RightMotionController->SetTrackingSource(EControllerHand::Right);
}

void AVRLab26VRCharacter::BeginPlay()
{
	Super::BeginPlay();
}
