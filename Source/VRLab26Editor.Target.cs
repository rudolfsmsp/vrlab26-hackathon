// Copyright VRLab26 Hackathon. All Rights Reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class VRLab26EditorTarget : TargetRules
{
	public VRLab26EditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.V5;
		IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_5;
		ExtraModuleNames.Add("VRLab26");
	}
}
