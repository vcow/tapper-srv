package
{
	import feathers.utils.ScreenDensityScaleFactorManager;

	import flash.display.MovieClip;
	import flash.display.StageAlign;
	import flash.display.StageScaleMode;
	import flash.events.Event;

	import starling.core.Starling;

	[SWF(frameRate="60", backgroundColor="#000000")]
	public class Main extends MovieClip
	{
		public function Main()
		{
			super();

			if (stage)
			{
				init();
			}
			else
			{
				addEventListener(Event.ADDED_TO_STAGE, onAddedToStage);
			}
		}

		private function onAddedToStage(event:Event):void
		{
			removeEventListener(Event.ADDED_TO_STAGE, onAddedToStage);
			init();
		}

		private function init():void
		{
			stage.scaleMode = StageScaleMode.NO_SCALE;
			stage.align = StageAlign.TOP_LEFT;
			var starling:Starling = new Starling(View, stage);
			new ScreenDensityScaleFactorManager(starling);
			starling.start();
		}
	}
}
