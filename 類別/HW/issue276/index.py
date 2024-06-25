import psycopg2
import data

def main():

    conn = psycopg2.connect("postgresql://tvdi_vf7z_user:JCgL4deGUYueFydNQFkCViaj3DFeYZNC@dpg-cpscsm2j1k6c738l6m50-a.singapore-postgres.render.com/tvdi_vf7z")
    with conn: 
        with conn.cursor() as cursor: 
            sql='''
            CREATE TABLE IF NOT EXISTS youbike (
            _id Serial Primary Key,
            sna VARCHAR(50) NOT NULL,
            sarea VARCHAR(50),
            ar VARCHAR(100),
            mday timestamp,
            updateTime timestamp,
            total SMALLINT,
            rent_bikes SMALLINT,
            return_bikes SMALLINT,
            lat REAL,
            lng REAL,
            act boolean,
            UNIQUE(sna, updateTime)  -- Add unique constraint on sna and updateTime
            );
            '''
            cursor.execute(sql)

        all_data = data.load_data()

        with conn.cursor() as cursor:
            insert_sql='''
            INSERT INTO youbike(sna,sarea,ar,mday,updateTime,total,rent_bikes,return_bikes,lat,lng,act)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (sna, updateTime) DO NOTHING;  -- Handle conflict with DO NOTHING
            '''
            for site in all_data:
                cursor.execute(insert_sql,(site['sna'],
                                           site['sarea'],
                                           site['ar'],
                                           site['mday'],
                                           site['updateTime'],
                                           site['total'],
                                           site['rent_bikes'],
                                           site['return_bikes'],  # Fixed typo 'retuen_bikes' to 'return_bikes'
                                           site['lat'],
                                           site['lng'],
                                           site['act']
                                           ))     
    conn.close()

if __name__ == '__main__':
    main()
