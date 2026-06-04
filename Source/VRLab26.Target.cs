// Copyright VRLab26 Hackathon. All Rights Reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class VRLab26Target : TargetRules
{
	public VRLab26Target(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.V5;
		IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_5;
		ExtraModuleNames.Add("VRLab26");
	}
}
