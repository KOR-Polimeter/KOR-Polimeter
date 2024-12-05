package com.KOR_Polimeter.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
@RequestMapping("/api")
public class ChartController {

    @Autowired
    private RestTemplate restTemplate;

    @GetMapping("/chart/{pol_id}")
    public ResponseEntity<String> getChart(@PathVariable int pol_id) {
        String flaskUrl = "http://127.0.0.1:5000/api/chart/" + pol_id;
        ResponseEntity<String> response = restTemplate.getForEntity(flaskUrl, String.class);

        // JSON 응답으로 반환
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON); // JSON 타입으로 명시

        return ResponseEntity.ok().headers(headers).body(response.getBody());
    }
}




