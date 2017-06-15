package
{
	import feathers.controls.LayoutGroup;
	import feathers.themes.MetalWorksDesktopTheme;

	public class ViewBase extends LayoutGroup
	{
		public function ViewBase()
		{
			super();
			new MetalWorksDesktopTheme();
		}
	}
}
