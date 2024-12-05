package com.KOR_Polimeter.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class ChartService {

    @Autowired
    private RestTemplate restTemplate;

    public String generateChart(int pol_id) {
        // 플라스크 서버 URL
        String flaskApiUrl = "http://127.0.0.1:5000/api/chart/" + pol_id;

        // GET 요청 보내기
        ResponseEntity<String> response = restTemplate.exchange(
                flaskApiUrl,
                HttpMethod.GET,
                null,
                String.class
        );

        // 응답 내용 확인
        return response.getBody(); // 차트 이미지 경로 또는 실패 메시지
    }
}