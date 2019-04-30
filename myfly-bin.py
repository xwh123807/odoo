__import__('os').environ['TZ'] = 'UTC'
import myfly

if __name__ == "__main__":
    myfly.cli.main()