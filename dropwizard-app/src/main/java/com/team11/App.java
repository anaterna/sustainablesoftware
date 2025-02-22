package com.team11;

import com.team11.resources.GalleryResource;
import io.dropwizard.assets.AssetsBundle;
import io.dropwizard.core.Application;
import io.dropwizard.core.setup.Bootstrap;
import io.dropwizard.core.setup.Environment;

public class App extends Application<Config> {

    public static void main(final String[] args) throws Exception {
        new App().run(args);
    }

    @Override
    public void initialize(final Bootstrap<Config> bootstrap) {
        bootstrap.addBundle(new AssetsBundle("/assets/", "/static/", null, ""));
    }

    @Override
    public void run(final Config configuration,
                    final Environment environment) {
        environment.jersey().register(new GalleryResource());
    }

}
