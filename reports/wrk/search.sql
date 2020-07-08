SELECT u.id               u_id,
       u.name             u_name,
       u.last_name        u_last_name,
       u.email            u_email,
       u.password         u_password,
       u.birth_date       u_birth_date,
       u.gender           u_gender,
       u.interests        u_interests,
       u.city             u_city,
       f.id               f_id,
       f.follower_user_id f_follower_user_id,
       f.followed_user_id f_followed_user_id,
       f.status           f_status


FROM user u
LEFT JOIN follower f
ON
    (
        u.id = f.follower_user_id
        OR u.id = f.followed_user_id
    )
    AND
    (
        f.follower_user_id = 1
        OR f.followed_user_id = 1
    )
    AND
        u.id != 1
WHERE u.last_name LIKE 'Ly%' AND u.name LIKE 'Me%'
ORDER BY u.id ASC
LIMIT 10