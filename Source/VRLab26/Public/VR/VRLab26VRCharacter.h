// Copyright VRLab26 Hackathon. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "VRLab26VRCharacter.generated.h"

class UCameraComponent;
class UMotionControllerComponent;

UCLASS()
class VRLAB26_API AVRLab26VRCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	AVRLab26VRCharacter();

protected:
	virtual void BeginPlay() override;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "VR")
	TObjectPtr<UCameraComponent> VRCamera;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "VR")
	TObjectPtr<UMotionControllerComponent> LeftMotionController;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "VR")
	TObjectPtr<UMotionControllerComponent> RightMotionController;
};
