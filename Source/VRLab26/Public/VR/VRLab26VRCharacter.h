// Copyright VRLab26 Hackathon. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "VRLab26VRCharacter.generated.h"

class UCameraComponent;
class UMotionControllerComponent;

/**
 * OpenXR VR pawn tuned for Meta Quest 2/3 (Link and standalone).
 * Uses OpenXR Grip motion sources recommended by Meta for controller tracking.
 */
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

	/** Controller grip pose — attach held objects here. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "VR|Quest")
	TObjectPtr<UMotionControllerComponent> LeftGripController;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "VR|Quest")
	TObjectPtr<UMotionControllerComponent> RightGripController;

	/** Controller aim pose — use for line traces / UI pointers. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "VR|Quest")
	TObjectPtr<UMotionControllerComponent> LeftAimController;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "VR|Quest")
	TObjectPtr<UMotionControllerComponent> RightAimController;

private:
	void ConfigureMotionController(UMotionControllerComponent* Component, FName MotionSource) const;
};
