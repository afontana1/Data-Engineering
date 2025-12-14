<?php

function outputGuitars($guitar)
{
    echo '<pre>';
    print_r($guitar);
    echo '<pre>';
}


function pluck($arr, $key)
{
    $guitar = array_map(function ($arr) use ($key) {
        return $arr[$key];
    }, $arr);

    return $guitar;
}