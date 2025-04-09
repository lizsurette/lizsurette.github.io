import os
import shutil
import logging

logger = logging.getLogger(__name__)

def copy_static_assets():
    """
    Copy static assets to the _site directory.
    
    This function is used during site generation to copy static assets
    from the app/static directory to the _site/static directory.
    """
    try:
        # Create _site/static directory if it doesn't exist
        site_static_dir = os.path.join('_site', 'static')
        if not os.path.exists(site_static_dir):
            os.makedirs(site_static_dir)
        
        # Copy static assets
        app_static_dir = os.path.join('app', 'static')
        if os.path.exists(app_static_dir):
            for item in os.listdir(app_static_dir):
                src = os.path.join(app_static_dir, item)
                dst = os.path.join(site_static_dir, item)
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            logger.info(f"Static assets copied to {site_static_dir}")
    except Exception as e:
        logger.error(f"Error copying static assets: {e}") 