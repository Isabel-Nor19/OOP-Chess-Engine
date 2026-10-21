package io.github.Isabelnorton;

import com.badlogic.gdx.ApplicationAdapter;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.Input.Keys;

/** {@link com.badlogic.gdx.ApplicationListener} implementation shared by all platforms. */
public class Main extends ApplicationAdapter {
    private SpriteBatch batch;
    private Texture image;

    private int x = 20;
    private int y = 20;
    private int sprite_second = 600; 

    private int sprite_width = 64;
    private int sprite_height = 64;

    @Override
    public void create() {
        batch = new SpriteBatch();
        image = new Texture("sprite_man.png");
    }

    @Override
    public void render() {
        float deltaTime = Gdx.graphics.getDeltaTime();

        if (Gdx.input.isKeyPressed(Keys.A)) {
            x -= sprite_second * deltaTime;
        }
        if (Gdx.input.isKeyPressed(Keys.D)) {
            x += sprite_second * deltaTime;
        }      
        if (Gdx.input.isKeyPressed(Keys.W)) {
            y += sprite_second * deltaTime;
        }
        if (Gdx.input.isKeyPressed(Keys.S)) {
            y -= sprite_second * deltaTime;
        }      

        ScreenUtils.clear(0.15f, 0.15f, 0.2f, 1f);
        batch.begin();
        batch.draw(image, x, y, sprite_width, sprite_height);
        batch.end();
    }

    @Override
    public void dispose() {
        batch.dispose();
        image.dispose();
    }
}
