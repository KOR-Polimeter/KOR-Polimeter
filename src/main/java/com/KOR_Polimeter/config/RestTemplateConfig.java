package com.KOR_Polimeter.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class RestTemplateConfig {

    // RestTemplate 빈을 등록하는 메서드
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
