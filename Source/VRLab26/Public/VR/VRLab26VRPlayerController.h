// Copyright VRLab26 Hackathon. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "VRLab26VRPlayerController.generated.h"

UCLASS()
class VRLAB26_API AVRLab26VRPlayerController : public APlayerController
{
	GENERATED_BODY()

public:
	AVRLab26VRPlayerController();

protected:
	virtual void BeginPlay() override;
};
