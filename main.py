import argparse
from signal_untangler.algorithm import is_interweaving

def main():
    parser = argparse.ArgumentParser(description='Signal Untangler - Pattern Interweaving Detector')
    
    # Add subparsers for different modes
    subparsers = parser.add_subparsers(dest='mode', help='Operation mode')
    
    # GUI mode
    gui_parser = subparsers.add_parser('gui', help='Launch graphical user interface')
    
    # CLI mode
    cli_parser = subparsers.add_parser('cli', help='Run in command line mode')
    cli_parser.add_argument('-s', '--signal', required=True, help='Signal string to analyze')
    cli_parser.add_argument('-x', '--pattern-x', required=True, help='First pattern to check for interweaving')
    cli_parser.add_argument('-y', '--pattern-y', required=True, help='Second pattern to check for interweaving')
    
    args = parser.parse_args()
    
    # Handle different modes
    if args.mode == 'gui':
        # Import GUI module only when needed
        from signal_untangler_gui.app import launch_gui
        launch_gui()
    elif args.mode == 'cli':
        result = is_interweaving(args.signal, args.pattern_x, args.pattern_y)
        if result:
            print(f"SUCCESS: '{args.signal}' IS an interweaving of patterns '{args.pattern_x}' and '{args.pattern_y}'")
        else:
            print(f"FAILURE: '{args.signal}' is NOT an interweaving of patterns '{args.pattern_x}' and '{args.pattern_y}'")
    else:
        # Default to GUI if no mode specified
        from interweaving_gui.app import launch_gui
        launch_gui()

if __name__ == "__main__":
    main()
