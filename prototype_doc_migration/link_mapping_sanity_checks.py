import json
import os.path

path_to_docs = 'C:\\Users\\Erik\\Documents\\GitHub\\Factorio\\scripts\\lua_doc\\doc-files'

wiki_links_types = ['https://wiki.factorio.com/Types/ActivateEquipmentCapsuleAction', 'https://wiki.factorio.com/Types/ActivityBarStyleSpecification', 'https://wiki.factorio.com/Types/AmmoDamageModifierPrototype', 'https://wiki.factorio.com/Types/AmmoSourceType', 'https://wiki.factorio.com/Types/AmmoType', 'https://wiki.factorio.com/Types/AnimatedVector', 'https://wiki.factorio.com/Types/Animation', 'https://wiki.factorio.com/Types/Animation4Way', 'https://wiki.factorio.com/Types/AnimationElement', 'https://wiki.factorio.com/Types/AnimationFrameSequence', 'https://wiki.factorio.com/Types/AnimationVariations', 'https://wiki.factorio.com/Types/AreaTriggerItem', 'https://wiki.factorio.com/Types/ArtilleryRemoteCapsuleAction', 'https://wiki.factorio.com/Types/ArtilleryTriggerDelivery', 'https://wiki.factorio.com/Types/AttackParameters', 'https://wiki.factorio.com/Types/AttackReaction', 'https://wiki.factorio.com/Types/AttackReactionItem', 'https://wiki.factorio.com/Types/AutoplaceSpecification', 'https://wiki.factorio.com/Types/BaseAttackParameters', 'https://wiki.factorio.com/Types/BeaconGraphicsSet', 'https://wiki.factorio.com/Types/BeaconModuleVisualization', 'https://wiki.factorio.com/Types/BeaconModuleVisualizations', 'https://wiki.factorio.com/Types/BeamAttackParameters', 'https://wiki.factorio.com/Types/BeamTriggerDelivery', 'https://wiki.factorio.com/Types/BlendMode', 'https://wiki.factorio.com/Types/BoolModifierPrototype', 'https://wiki.factorio.com/Types/BorderImageSet', 'https://wiki.factorio.com/Types/BoundingBox', 'https://wiki.factorio.com/Types/BoxSpecification', 'https://wiki.factorio.com/Types/ButtonStyleSpecification', 'https://wiki.factorio.com/Types/CameraEffectTriggerEffectItem', 'https://wiki.factorio.com/Types/CameraStyleSpecification', 'https://wiki.factorio.com/Types/CapsuleAction', 'https://wiki.factorio.com/Types/CharacterArmorAnimation', 'https://wiki.factorio.com/Types/CheckBoxStyleSpecification', 'https://wiki.factorio.com/Types/CircuitConnectorSprites', 'https://wiki.factorio.com/Types/CircularParticleCreationSpecification', 'https://wiki.factorio.com/Types/CircularProjectileCreationSpecification', 'https://wiki.factorio.com/Types/ClusterTriggerItem', 'https://wiki.factorio.com/Types/CollisionMask', 'https://wiki.factorio.com/Types/Color', 'https://wiki.factorio.com/Types/ConnectableEntityGraphics', 'https://wiki.factorio.com/Types/ConsumingType', 'https://wiki.factorio.com/Types/CreateDecorativesTriggerEffectItem', 'https://wiki.factorio.com/Types/CreateEntityTriggerEffectItem', 'https://wiki.factorio.com/Types/CreateExplosionTriggerEffectItem', 'https://wiki.factorio.com/Types/CreateFireTriggerEffectItem', 'https://wiki.factorio.com/Types/CreateParticleTriggerEffectItem', 'https://wiki.factorio.com/Types/CreateSmokeTriggerEffectItem', 'https://wiki.factorio.com/Types/CreateStickerTriggerEffectItem', 'https://wiki.factorio.com/Types/CreateTrivialSmokeEffectItem', 'https://wiki.factorio.com/Types/CursorBoxType', 'https://wiki.factorio.com/Types/CyclicSound', 'https://wiki.factorio.com/Types/DamagePrototype', 'https://wiki.factorio.com/Types/DamageTriggerEffectItem', 'https://wiki.factorio.com/Types/DamageTypeFilters', 'https://wiki.factorio.com/Types/DaytimeColorLookupTable', 'https://wiki.factorio.com/Types/DestroyCliffsCapsuleAction', 'https://wiki.factorio.com/Types/DestroyCliffsTriggerEffectItem', 'https://wiki.factorio.com/Types/DestroyDecorativesTriggerEffectItem', 'https://wiki.factorio.com/Types/DirectTriggerItem', 'https://wiki.factorio.com/Types/Direction', 'https://wiki.factorio.com/Types/DoubleSliderStyleSpecification', 'https://wiki.factorio.com/Types/DropDownStyleSpecification', 'https://wiki.factorio.com/Types/Effect', 'https://wiki.factorio.com/Types/EffectTypeLimitation', 'https://wiki.factorio.com/Types/ElectricUsagePriority', 'https://wiki.factorio.com/Types/ElementImageSet', 'https://wiki.factorio.com/Types/ElementImageSetLayer', 'https://wiki.factorio.com/Types/EmptyWidgetStyleSpecification', 'https://wiki.factorio.com/Types/Energy', 'https://wiki.factorio.com/Types/EnergySource', 'https://wiki.factorio.com/Types/EntityPrototypeFlags', 'https://wiki.factorio.com/Types/EquipmentShape', 'https://wiki.factorio.com/Types/ExplosionDefinition', 'https://wiki.factorio.com/Types/FileName', 'https://wiki.factorio.com/Types/FlameThrowerExplosionTriggerDelivery', 'https://wiki.factorio.com/Types/FlowStyleSpecification', 'https://wiki.factorio.com/Types/FluidBox', 'https://wiki.factorio.com/Types/FluidIngredientPrototype', 'https://wiki.factorio.com/Types/FluidProductPrototype', 'https://wiki.factorio.com/Types/FootprintParticle', 'https://wiki.factorio.com/Types/FootstepTriggerEffectList', 'https://wiki.factorio.com/Types/ForceCondition', 'https://wiki.factorio.com/Types/FrameStyleSpecification', 'https://wiki.factorio.com/Types/GiveItemModifierPrototype', 'https://wiki.factorio.com/Types/GlowStyleSpecification', 'https://wiki.factorio.com/Types/GraphStyleSpecification', 'https://wiki.factorio.com/Types/GraphicsVariation', 'https://wiki.factorio.com/Types/GunSpeedModifierPrototype', 'https://wiki.factorio.com/Types/HeatBuffer', 'https://wiki.factorio.com/Types/HeatConnection', 'https://wiki.factorio.com/Types/HorizontalFlowStyleSpecification', 'https://wiki.factorio.com/Types/HorizontalScrollBarStyleSpecification', 'https://wiki.factorio.com/Types/IconData', 'https://wiki.factorio.com/Types/IconSpecification', 'https://wiki.factorio.com/Types/ImageStyleSpecification', 'https://wiki.factorio.com/Types/IngredientPrototype', 'https://wiki.factorio.com/Types/InsertItemTriggerEffectItem', 'https://wiki.factorio.com/Types/InstantTriggerDelivery', 'https://wiki.factorio.com/Types/InterruptibleSound', 'https://wiki.factorio.com/Types/InvokeTileEffectTriggerEffectItem', 'https://wiki.factorio.com/Types/ItemCountType', 'https://wiki.factorio.com/Types/ItemIngredientPrototype', 'https://wiki.factorio.com/Types/ItemProductPrototype', 'https://wiki.factorio.com/Types/ItemPrototypeFlags', 'https://wiki.factorio.com/Types/ItemStackIndex', 'https://wiki.factorio.com/Types/ItemToPlace', 'https://wiki.factorio.com/Types/LabelStyleSpecification', 'https://wiki.factorio.com/Types/LayeredSound', 'https://wiki.factorio.com/Types/LightDefinition', 'https://wiki.factorio.com/Types/LightFlickeringDefinition', 'https://wiki.factorio.com/Types/LineStyleSpecification', 'https://wiki.factorio.com/Types/LineTriggerItem', 'https://wiki.factorio.com/Types/ListBoxStyleSpecification', 'https://wiki.factorio.com/Types/LocalisedString', 'https://wiki.factorio.com/Types/Loot', 'https://wiki.factorio.com/Types/MapGenPreset', 'https://wiki.factorio.com/Types/MapGenSize', 'https://wiki.factorio.com/Types/MaterialAmountType', 'https://wiki.factorio.com/Types/MinableProperties', 'https://wiki.factorio.com/Types/MinimapStyleSpecification', 'https://wiki.factorio.com/Types/MiningDrillGraphicsSet', 'https://wiki.factorio.com/Types/ModifierPrototype', 'https://wiki.factorio.com/Types/ModuleSpecification', 'https://wiki.factorio.com/Types/NestedTriggerEffectItem', 'https://wiki.factorio.com/Types/NoiseExpression', 'https://wiki.factorio.com/Types/NothingModifierPrototype', 'https://wiki.factorio.com/Types/Order', 'https://wiki.factorio.com/Types/OrientedCliffPrototype', 'https://wiki.factorio.com/Types/PipeConnectionDefinition', 'https://wiki.factorio.com/Types/PlaceAsTile', 'https://wiki.factorio.com/Types/PlaySoundTriggerEffectItem', 'https://wiki.factorio.com/Types/Position', 'https://wiki.factorio.com/Types/ProductPrototype', 'https://wiki.factorio.com/Types/ProgressBarStyleSpecification', 'https://wiki.factorio.com/Types/ProjectileAttackParameters', 'https://wiki.factorio.com/Types/ProjectileTriggerDelivery', 'https://wiki.factorio.com/Types/PumpConnectorGraphics', 'https://wiki.factorio.com/Types/PushBackTriggerEffectItem', 'https://wiki.factorio.com/Types/RadioButtonStyleSpecification', 'https://wiki.factorio.com/Types/RadiusVisualisationSpecification', 'https://wiki.factorio.com/Types/RailPieceLayers', 'https://wiki.factorio.com/Types/RealOrientation', 'https://wiki.factorio.com/Types/RenderLayer', 'https://wiki.factorio.com/Types/Resistances', 'https://wiki.factorio.com/Types/RotatedAnimation', 'https://wiki.factorio.com/Types/RotatedAnimation4Way', 'https://wiki.factorio.com/Types/RotatedAnimationVariations', 'https://wiki.factorio.com/Types/RotatedSprite', 'https://wiki.factorio.com/Types/ScriptTriggerEffectItem', 'https://wiki.factorio.com/Types/ScrollBarStyleSpecification', 'https://wiki.factorio.com/Types/ScrollPaneStyleSpecification', 'https://wiki.factorio.com/Types/SetTileTriggerEffectItem', 'https://wiki.factorio.com/Types/ShowExplosionOnChartTriggerEffectItem', 'https://wiki.factorio.com/Types/SignalColorMapping', 'https://wiki.factorio.com/Types/SignalIDConnector', 'https://wiki.factorio.com/Types/SimpleModifierPrototype', 'https://wiki.factorio.com/Types/SimulationDefinition', 'https://wiki.factorio.com/Types/SliderStyleSpecification', 'https://wiki.factorio.com/Types/SmokeSource', 'https://wiki.factorio.com/Types/Sound', 'https://wiki.factorio.com/Types/SpawnPoint', 'https://wiki.factorio.com/Types/SpeechBubbleStyleSpecification', 'https://wiki.factorio.com/Types/SpiderEnginePrototype', 'https://wiki.factorio.com/Types/SpiderLegGraphicsSet', 'https://wiki.factorio.com/Types/SpiderLegPart', 'https://wiki.factorio.com/Types/SpiderLegSpecification', 'https://wiki.factorio.com/Types/SpiderVehicleGraphicsSet', 'https://wiki.factorio.com/Types/Sprite', 'https://wiki.factorio.com/Types/Sprite4Way', 'https://wiki.factorio.com/Types/Sprite8Way', 'https://wiki.factorio.com/Types/SpriteFlags', 'https://wiki.factorio.com/Types/SpriteNWaySheet', 'https://wiki.factorio.com/Types/SpritePriority', 'https://wiki.factorio.com/Types/SpriteSizeType', 'https://wiki.factorio.com/Types/SpriteVariations', 'https://wiki.factorio.com/Types/StreamAttackParameters', 'https://wiki.factorio.com/Types/StreamTriggerDelivery', 'https://wiki.factorio.com/Types/StretchRule', 'https://wiki.factorio.com/Types/Stripe', 'https://wiki.factorio.com/Types/StyleSpecification', 'https://wiki.factorio.com/Types/StyleWithClickableGraphicalSetSpecification', 'https://wiki.factorio.com/Types/SwitchStyleSpecification', 'https://wiki.factorio.com/Types/TabStyleSpecification', 'https://wiki.factorio.com/Types/TabbedPaneStyleSpecification', 'https://wiki.factorio.com/Types/TableStyleSpecification', 'https://wiki.factorio.com/Types/TechnologySlotStyleSpecification', 'https://wiki.factorio.com/Types/TextBoxStyleSpecification', 'https://wiki.factorio.com/Types/ThrowCapsuleAction', 'https://wiki.factorio.com/Types/TileSprite', 'https://wiki.factorio.com/Types/TileTransitionSprite', 'https://wiki.factorio.com/Types/TileTransitions', 'https://wiki.factorio.com/Types/TipStatus', 'https://wiki.factorio.com/Types/TipTrigger', 'https://wiki.factorio.com/Types/TransportBeltConnectorFrame', 'https://wiki.factorio.com/Types/TreePrototypeVariation', 'https://wiki.factorio.com/Types/Trigger', 'https://wiki.factorio.com/Types/TriggerDelivery', 'https://wiki.factorio.com/Types/TriggerEffect', 'https://wiki.factorio.com/Types/TriggerEffectItem', 'https://wiki.factorio.com/Types/TriggerItem', 'https://wiki.factorio.com/Types/TriggerTargetMask', 'https://wiki.factorio.com/Types/TurretAttackModifierPrototype', 'https://wiki.factorio.com/Types/UnitAISettings', 'https://wiki.factorio.com/Types/UnitSpawnDefinition', 'https://wiki.factorio.com/Types/UnlockRecipeModifierPrototype', 'https://wiki.factorio.com/Types/UseOnSelfCapsuleAction', 'https://wiki.factorio.com/Types/Vector3D', 'https://wiki.factorio.com/Types/VerticalFlowStyleSpecification', 'https://wiki.factorio.com/Types/VerticalScrollBarStyleSpecification', 'https://wiki.factorio.com/Types/WaterReflectionDefinition', 'https://wiki.factorio.com/Types/WireConnectionPoint', 'https://wiki.factorio.com/Types/WirePosition', 'https://wiki.factorio.com/Types/WorkingSound', 'https://wiki.factorio.com/Types/WorkingVisualisation', 'https://wiki.factorio.com/Types/bool', 'https://wiki.factorio.com/Types/double', 'https://wiki.factorio.com/Types/float', 'https://wiki.factorio.com/Types/int16', 'https://wiki.factorio.com/Types/int32', 'https://wiki.factorio.com/Types/int64', 'https://wiki.factorio.com/Types/int8', 'https://wiki.factorio.com/Types/string', 'https://wiki.factorio.com/Types/table', 'https://wiki.factorio.com/Types/uint16', 'https://wiki.factorio.com/Types/uint32', 'https://wiki.factorio.com/Types/uint64', 'https://wiki.factorio.com/Types/uint8', 'https://wiki.factorio.com/Types/vector']

wiki_links_prototypes = ['https://wiki.factorio.com/Prototype/Accumulator', 'https://wiki.factorio.com/Prototype/Achievement', 'https://wiki.factorio.com/Prototype/ActiveDefenseEquipment', 'https://wiki.factorio.com/Prototype/AmbientSound', 'https://wiki.factorio.com/Prototype/AmmoCategory', 'https://wiki.factorio.com/Prototype/AmmoItem', 'https://wiki.factorio.com/Prototype/AmmoTurret', 'https://wiki.factorio.com/Prototype/Animation', 'https://wiki.factorio.com/Prototype/ArithmeticCombinator', 'https://wiki.factorio.com/Prototype/Armor', 'https://wiki.factorio.com/Prototype/Arrow', 'https://wiki.factorio.com/Prototype/ArtilleryFlare', 'https://wiki.factorio.com/Prototype/ArtilleryProjectile', 'https://wiki.factorio.com/Prototype/ArtilleryTurret', 'https://wiki.factorio.com/Prototype/ArtilleryWagon', 'https://wiki.factorio.com/Prototype/AssemblingMachine', 'https://wiki.factorio.com/Prototype/AutoplaceControl', 'https://wiki.factorio.com/Prototype/BatteryEquipment', 'https://wiki.factorio.com/Prototype/Beacon', 'https://wiki.factorio.com/Prototype/Beam', 'https://wiki.factorio.com/Prototype/BeltImmunityEquipment', 'https://wiki.factorio.com/Prototype/BlueprintBook', 'https://wiki.factorio.com/Prototype/BlueprintItem', 'https://wiki.factorio.com/Prototype/Boiler', 'https://wiki.factorio.com/Prototype/BuildEntityAchievement', 'https://wiki.factorio.com/Prototype/BurnerGenerator', 'https://wiki.factorio.com/Prototype/Capsule', 'https://wiki.factorio.com/Prototype/Car', 'https://wiki.factorio.com/Prototype/CargoWagon', 'https://wiki.factorio.com/Prototype/Character', 'https://wiki.factorio.com/Prototype/CharacterCorpse', 'https://wiki.factorio.com/Prototype/Cliff', 'https://wiki.factorio.com/Prototype/CombatRobot', 'https://wiki.factorio.com/Prototype/CombatRobotCountAchievement', 'https://wiki.factorio.com/Prototype/Combinator', 'https://wiki.factorio.com/Prototype/ConstantCombinator', 'https://wiki.factorio.com/Prototype/ConstructWithRobotsAchievement', 'https://wiki.factorio.com/Prototype/ConstructionRobot', 'https://wiki.factorio.com/Prototype/Container', 'https://wiki.factorio.com/Prototype/CopyPasteTool', 'https://wiki.factorio.com/Prototype/Corpse', 'https://wiki.factorio.com/Prototype/CraftingMachine', 'https://wiki.factorio.com/Prototype/CurvedRail', 'https://wiki.factorio.com/Prototype/CustomInput', 'https://wiki.factorio.com/Prototype/DamageType', 'https://wiki.factorio.com/Prototype/DeciderCombinator', 'https://wiki.factorio.com/Prototype/DeconstructWithRobotsAchievement', 'https://wiki.factorio.com/Prototype/DeconstructibleTileProxy', 'https://wiki.factorio.com/Prototype/DeconstructionItem', 'https://wiki.factorio.com/Prototype/Decorative', 'https://wiki.factorio.com/Prototype/DeliverByRobotsAchievement', 'https://wiki.factorio.com/Prototype/DontBuildEntityAchievement', 'https://wiki.factorio.com/Prototype/DontCraftManuallyAchievement', 'https://wiki.factorio.com/Prototype/DontUseEntityInEnergyProductionAchievement', 'https://wiki.factorio.com/Prototype/EditorController', 'https://wiki.factorio.com/Prototype/ElectricEnergyInterface', 'https://wiki.factorio.com/Prototype/ElectricPole', 'https://wiki.factorio.com/Prototype/ElectricTurret', 'https://wiki.factorio.com/Prototype/EnemySpawner', 'https://wiki.factorio.com/Prototype/EnergyShieldEquipment', 'https://wiki.factorio.com/Prototype/Entity', 'https://wiki.factorio.com/Prototype/EntityGhost', 'https://wiki.factorio.com/Prototype/EntityParticle', 'https://wiki.factorio.com/Prototype/EntityWithHealth', 'https://wiki.factorio.com/Prototype/EntityWithOwner', 'https://wiki.factorio.com/Prototype/Equipment', 'https://wiki.factorio.com/Prototype/EquipmentCategory', 'https://wiki.factorio.com/Prototype/EquipmentGrid', 'https://wiki.factorio.com/Prototype/Explosion', 'https://wiki.factorio.com/Prototype/FinishTheGameAchievement', 'https://wiki.factorio.com/Prototype/FireFlame', 'https://wiki.factorio.com/Prototype/Fish', 'https://wiki.factorio.com/Prototype/FlameThrowerExplosion', 'https://wiki.factorio.com/Prototype/Fluid', 'https://wiki.factorio.com/Prototype/FluidStream', 'https://wiki.factorio.com/Prototype/FluidTurret', 'https://wiki.factorio.com/Prototype/FluidWagon', 'https://wiki.factorio.com/Prototype/FlyingRobot', 'https://wiki.factorio.com/Prototype/FlyingText', 'https://wiki.factorio.com/Prototype/Font', 'https://wiki.factorio.com/Prototype/FuelCategory', 'https://wiki.factorio.com/Prototype/Furnace', 'https://wiki.factorio.com/Prototype/Gate', 'https://wiki.factorio.com/Prototype/Generator', 'https://wiki.factorio.com/Prototype/GeneratorEquipment', 'https://wiki.factorio.com/Prototype/GodController', 'https://wiki.factorio.com/Prototype/GroupAttackAchievement', 'https://wiki.factorio.com/Prototype/GuiStyle', 'https://wiki.factorio.com/Prototype/Gun', 'https://wiki.factorio.com/Prototype/HeatInterface', 'https://wiki.factorio.com/Prototype/HeatPipe', 'https://wiki.factorio.com/Prototype/HighlightBoxEntity', 'https://wiki.factorio.com/Prototype/InfinityContainer', 'https://wiki.factorio.com/Prototype/InfinityPipe', 'https://wiki.factorio.com/Prototype/Inserter', 'https://wiki.factorio.com/Prototype/Item', 'https://wiki.factorio.com/Prototype/ItemEntity', 'https://wiki.factorio.com/Prototype/ItemGroup', 'https://wiki.factorio.com/Prototype/ItemRequestProxy', 'https://wiki.factorio.com/Prototype/ItemSubGroup', 'https://wiki.factorio.com/Prototype/ItemWithEntityData', 'https://wiki.factorio.com/Prototype/ItemWithInventory', 'https://wiki.factorio.com/Prototype/ItemWithLabel', 'https://wiki.factorio.com/Prototype/ItemWithTags', 'https://wiki.factorio.com/Prototype/KillAchievement', 'https://wiki.factorio.com/Prototype/Lab', 'https://wiki.factorio.com/Prototype/Lamp', 'https://wiki.factorio.com/Prototype/LandMine', 'https://wiki.factorio.com/Prototype/LeafParticle', 'https://wiki.factorio.com/Prototype/LinkedBelt', 'https://wiki.factorio.com/Prototype/LinkedContainer', 'https://wiki.factorio.com/Prototype/Loader1x1', 'https://wiki.factorio.com/Prototype/Loader1x2', 'https://wiki.factorio.com/Prototype/Locomotive', 'https://wiki.factorio.com/Prototype/LogisticContainer', 'https://wiki.factorio.com/Prototype/LogisticRobot', 'https://wiki.factorio.com/Prototype/MapGenPresets', 'https://wiki.factorio.com/Prototype/MapSettings', 'https://wiki.factorio.com/Prototype/Market', 'https://wiki.factorio.com/Prototype/MiningDrill', 'https://wiki.factorio.com/Prototype/MiningTool', 'https://wiki.factorio.com/Prototype/Module', 'https://wiki.factorio.com/Prototype/ModuleCategory', 'https://wiki.factorio.com/Prototype/MouseCursor', 'https://wiki.factorio.com/Prototype/MovementBonusEquipment', 'https://wiki.factorio.com/Prototype/NamedNoiseExpression', 'https://wiki.factorio.com/Prototype/NightVisionEquipment', 'https://wiki.factorio.com/Prototype/NoiseLayer', 'https://wiki.factorio.com/Prototype/OffshorePump', 'https://wiki.factorio.com/Prototype/Particle', 'https://wiki.factorio.com/Prototype/ParticleSource', 'https://wiki.factorio.com/Prototype/Pipe', 'https://wiki.factorio.com/Prototype/PipeToGround', 'https://wiki.factorio.com/Prototype/PlayerDamagedAchievement', 'https://wiki.factorio.com/Prototype/PlayerPort', 'https://wiki.factorio.com/Prototype/PowerSwitch', 'https://wiki.factorio.com/Prototype/ProduceAchievement', 'https://wiki.factorio.com/Prototype/ProducePerHourAchievement', 'https://wiki.factorio.com/Prototype/ProgrammableSpeaker', 'https://wiki.factorio.com/Prototype/Projectile', 'https://wiki.factorio.com/Prototype/Pump', 'https://wiki.factorio.com/Prototype/Radar', 'https://wiki.factorio.com/Prototype/Rail', 'https://wiki.factorio.com/Prototype/RailChainSignal', 'https://wiki.factorio.com/Prototype/RailPlanner', 'https://wiki.factorio.com/Prototype/RailRemnants', 'https://wiki.factorio.com/Prototype/RailSignal', 'https://wiki.factorio.com/Prototype/RailSignalBase', 'https://wiki.factorio.com/Prototype/Reactor', 'https://wiki.factorio.com/Prototype/Recipe', 'https://wiki.factorio.com/Prototype/RecipeCategory', 'https://wiki.factorio.com/Prototype/RepairTool', 'https://wiki.factorio.com/Prototype/ResearchAchievement', 'https://wiki.factorio.com/Prototype/ResourceCategory', 'https://wiki.factorio.com/Prototype/ResourceEntity', 'https://wiki.factorio.com/Prototype/Roboport', 'https://wiki.factorio.com/Prototype/RoboportEquipment', 'https://wiki.factorio.com/Prototype/RobotWithLogisticInterface', 'https://wiki.factorio.com/Prototype/RocketSilo', 'https://wiki.factorio.com/Prototype/RocketSiloRocket', 'https://wiki.factorio.com/Prototype/RocketSiloRocketShadow', 'https://wiki.factorio.com/Prototype/RollingStock', 'https://wiki.factorio.com/Prototype/SelectionTool', 'https://wiki.factorio.com/Prototype/Shortcut', 'https://wiki.factorio.com/Prototype/SimpleEntity', 'https://wiki.factorio.com/Prototype/SimpleEntityWithForce', 'https://wiki.factorio.com/Prototype/SimpleEntityWithOwner', 'https://wiki.factorio.com/Prototype/SimpleSmoke', 'https://wiki.factorio.com/Prototype/Smoke', 'https://wiki.factorio.com/Prototype/SmokeWithTrigger', 'https://wiki.factorio.com/Prototype/SolarPanel', 'https://wiki.factorio.com/Prototype/SolarPanelEquipment', 'https://wiki.factorio.com/Prototype/Sound', 'https://wiki.factorio.com/Prototype/SpectatorController', 'https://wiki.factorio.com/Prototype/SpeechBubble', 'https://wiki.factorio.com/Prototype/SpiderLeg', 'https://wiki.factorio.com/Prototype/SpiderVehicle', 'https://wiki.factorio.com/Prototype/SpidertronRemote', 'https://wiki.factorio.com/Prototype/Splitter', 'https://wiki.factorio.com/Prototype/Sprite', 'https://wiki.factorio.com/Prototype/Sticker', 'https://wiki.factorio.com/Prototype/StorageTank', 'https://wiki.factorio.com/Prototype/StraightRail', 'https://wiki.factorio.com/Prototype/Technology', 'https://wiki.factorio.com/Prototype/Tile', 'https://wiki.factorio.com/Prototype/TileEffect', 'https://wiki.factorio.com/Prototype/TileGhost', 'https://wiki.factorio.com/Prototype/TipsAndTricksItem', 'https://wiki.factorio.com/Prototype/TipsAndTricksItemCategory', 'https://wiki.factorio.com/Prototype/Tool', 'https://wiki.factorio.com/Prototype/TrainPathAchievement', 'https://wiki.factorio.com/Prototype/TrainStop', 'https://wiki.factorio.com/Prototype/TransportBelt', 'https://wiki.factorio.com/Prototype/TransportBeltConnectable', 'https://wiki.factorio.com/Prototype/Tree', 'https://wiki.factorio.com/Prototype/TriggerTargetType', 'https://wiki.factorio.com/Prototype/TrivialSmoke', 'https://wiki.factorio.com/Prototype/Turret', 'https://wiki.factorio.com/Prototype/Tutorial', 'https://wiki.factorio.com/Prototype/UndergroundBelt', 'https://wiki.factorio.com/Prototype/Unit', 'https://wiki.factorio.com/Prototype/UpgradeItem', 'https://wiki.factorio.com/Prototype/UtilityConstants', 'https://wiki.factorio.com/Prototype/UtilitySounds', 'https://wiki.factorio.com/Prototype/UtilitySprites', 'https://wiki.factorio.com/Prototype/Vehicle', 'https://wiki.factorio.com/Prototype/VirtualSignal', 'https://wiki.factorio.com/Prototype/Wall', 'https://wiki.factorio.com/Prototype/WindSound', 'https://wiki.factorio.com/PrototypeBase']

def find_missing(mapping, expected):
  for item in expected:
    if item not in mapping:
      print(item + ' missing from mapping.')

def find_extra(mapping, expected):
  for item in mapping:
    if item not in expected:
      print(item + ' extra in mapping (typo?).')
      
def check_links(mapping):
  new_links = []
  for new in mapping.values():
    if isinstance(new, str):
      if new not in new_links:
        new_links.append(new)
      else:
        print(new + ' is duplicate new link in mapping.')    
  
  for link in new_links:
    link_anchor = link.rfind('#')
    if link_anchor >= 0: 
      link = link[:link_anchor]
    link = link.removeprefix('https://lua-api.factorio.com/latest')
    if not os.path.isfile(path_to_docs + link):
      print(link + ' is not a valid file path.')

with open(os.path.dirname(__file__) + '/link_mapping.json', 'r') as f:
  link_mapping = json.load(f)

find_missing(link_mapping['types'], wiki_links_types)
find_extra(link_mapping['types'], wiki_links_types)
check_links(link_mapping['types'])

find_missing(link_mapping['prototypes'], wiki_links_prototypes)
find_extra(link_mapping['prototypes'], wiki_links_prototypes)
check_links(link_mapping['prototypes'])

# if new links is a boolean means the page does not exist on the new prototype docs
# if new link is False that means the page doesn't need to be kept on the wiki
# if new link is True that means the page is kept on the wiki because it's used by something not prototype docs