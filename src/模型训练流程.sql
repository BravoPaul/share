--odps sql
--********************************************************************--
--author:坤月
--create time:2019-12-30 16:44:03
--********************************************************************--

DROP TABLE IF EXISTS ytrec.ads_ykma_taopp_pointwise_features_rand_v2;
CREATE TABLE ytrec.ads_ykma_taopp_pointwise_features_rand_v2 AS
SELECT * FROM ytrec.ads_ykma_taopp_pointwise_features_v2
WHERE ds = MAX_PT('ytrec.ads_ykma_taopp_pointwise_features_v2')
ORDER BY RAND()
LIMIT 5000000;



drop table if exists ytrec.ads_ykma_taopp_pointwise_features_fillna_rand_v2;
drop table if exists ytrec.ads_ykma_taopp_pointwise_features_para_v2;
PAI -name FillMissingValues
 -project algo_public -Dlifecycle="7"
 -Dconfigs="type_ids,null,-1;pred_gender_ids,null,-1;pred_age_level_ids,null,-1;id_gender_ids,null,-1;id_constellation_ids,null,-1;pred_life_stage_hasbaby_ids,null,-1;pred_life_stage_marriednochild_ids,null,-1;id_zodiac_ids,null,-1;pred_life_stage_marriedhaschild_ids,null,-1;pred_life_stage_inlove_ids,null,-1;pred_life_stage_married_ids,null,-1;id_age,null,-1;pred_life_stage_haschild_ids,null,-1;pred_life_stage_ids,null,-1;tm_level_ids,null,-1;pred_life_stage_single_ids,null,-1;vip_level_name_ids,null,-1;pred_life_stage_marrying_ids,null,-1;pred_is_undergraduate_ids,null,-1;pred_education_degree_ids,null,-1;pred_school_ids,null,-1;pred_attending_college_ids,null,-1;pred_career_type_ids,null,-1;is_high_end_consumer_ids,null,-1;pred_has_pet_ids,null,-1;pred_has_car_ids,null,-1;pred_has_house_ids,null,-1;pred_car_series_ids,null,-1;car_brand_ids,null,-1;purchase_power_level_purchase_power_ids,null,-1;ip_prov_name_ids,null,-1;ip_city_name_ids,null,-1;common_receive_city_code_180d_ids,null,-1;common_receive_city_180d_ids,null,-1;common_receive_province_id_gw_180d_ids,null,-1;common_receive_province_gw_180d_ids,null,-1;common_receive_city_level_gw_180d_ids,null,-1;common_receive_district_id_gw_180d_ids,null,-1;common_receive_district_gw_180d_ids,null,-1;common_receive_city_code_gw_180d_ids,null,-1;common_receive_city_id_gw_180d_ids,null,-1;common_receive_city_name_gw_180d_ids,null,-1;tkm_level_ids,null,-1;tkm_level_title_ids,null,-1;point_ids,null,-1;is_has_eff_huabei_ids,null,-1;is_has_eff_88card_ids,null,-1;is_has_eff_card_ids,null,-1;is_has_eff_citycard_ids,null,-1;is_comm_master_ids,null,-1;tq_level_ids,null,-1;cate_id_ids,null,-1;cate_name_ids,null,-1;prefer_director_ids,null,-1;prefer_actors_ids,null,-1;prefer_type_ids,null,-1;prefer_distributor_ids,null,-1;prefer_country_ids,null,-1;prefer_language_ids,null,-1;prefer_version_ids,null,-1;pred_car_brand_ids,null,-1;card_pay_ord_cnt_1m,null,-1;card_pay_ord_cnt_2m,null,-1;card_pay_ord_cnt_3m,null,-1;card_pay_ord_cnt_6m,null,-1;card_pay_ord_cnt_1y,null,-1;card_pay_tkt_cnt_1m,null,-1;card_pay_tkt_cnt_2m,null,-1;card_pay_tkt_cnt_3m,null,-1;card_pay_tkt_cnt_6m,null,-1;card_pay_tkt_cnt_1y,null,-1;presale_pay_ord_cnt_1m,null,-1;presale_pay_ord_cnt_2m,null,-1;presale_pay_ord_cnt_3m,null,-1;presale_pay_ord_cnt_6m,null,-1;presale_pay_ord_cnt_1y,null,-1;discount_ord_cnt_1m,null,-1;discount_ord_cnt_2m,null,-1;discount_ord_cnt_3m,null,-1;discount_ord_cnt_6m,null,-1;discount_ord_cnt_1y,null,-1;pay_ord_cnt_1w,null,-1;pay_ord_cnt_2w,null,-1;pay_ord_cnt_1m,null,-1;pay_ord_cnt_2m,null,-1;pay_ord_cnt_3m,null,-1;pay_ord_cnt_6m,null,-1;pay_ord_cnt_1y,null,-1;pay_ord_cnt_td,null,-1;pay_ord_amt_1w,null,-1;pay_ord_amt_2w,null,-1;pay_ord_amt_1m,null,-1;pay_ord_amt_2m,null,-1;pay_ord_amt_3m,null,-1;pay_ord_amt_6m,null,-1;pay_ord_amt_1y,null,-1;pay_ord_amt_td,null,-1;pay_film_cnt_1w,null,-1;pay_film_cnt_2w,null,-1;pay_film_cnt_1m,null,-1;pay_film_cnt_2m,null,-1;pay_film_cnt_3m,null,-1;pay_film_cnt_6m,null,-1;pay_film_cnt_1y,null,-1;pay_film_cnt_td,null,-1;pay_cinema_cnt_1w,null,-1;pay_cinema_cnt_2w,null,-1;pay_cinema_cnt_1m,null,-1;pay_cinema_cnt_2m,null,-1;pay_cinema_cnt_3m,null,-1;pay_cinema_cnt_6m,null,-1;pay_cinema_cnt_1y,null,-1;pay_cinema_cnt_td,null,-1;pay_tkt_cnt_1w,null,-1;pay_tkt_cnt_2w,null,-1;pay_tkt_cnt_1m,null,-1;pay_tkt_cnt_2m,null,-1;pay_tkt_cnt_3m,null,-1;pay_tkt_cnt_6m,null,-1;pay_tkt_cnt_1y,null,-1;pay_tkt_cnt_td,null,-1;pay_tkt_sale_cnt_1w,null,-1;pay_tkt_sale_cnt_2w,null,-1;pay_tkt_sale_cnt_1m,null,-1;pay_tkt_sale_cnt_2m,null,-1;pay_tkt_sale_cnt_3m,null,-1;pay_tkt_sale_cnt_6m,null,-1;pay_tkt_sale_cnt_1y,null,-1;pay_tkt_sale_cnt_td,null,-1;pay_scd_cnt_1w,null,-1;pay_scd_cnt_2w,null,-1;pay_scd_cnt_1m,null,-1;pay_scd_cnt_2m,null,-1;pay_scd_cnt_3m,null,-1;pay_scd_cnt_6m,null,-1;pay_scd_cnt_1y,null,-1;pay_scd_cnt_td,null,-1;pay_scd_sale_cnt_1w,null,-1;pay_scd_sale_cnt_2w,null,-1;pay_scd_sale_cnt_1m,null,-1;pay_scd_sale_cnt_2m,null,-1;pay_scd_sale_cnt_3m,null,-1;pay_scd_sale_cnt_6m,null,-1;pay_scd_sale_cnt_1y,null,-1;pay_scd_sale_cnt_td,null,-1;pay_cinema_city_cnt_1w,null,-1;pay_cinema_city_cnt_2w,null,-1;pay_cinema_city_cnt_1m,null,-1;pay_cinema_city_cnt_2m,null,-1;pay_cinema_city_cnt_3m,null,-1;pay_cinema_city_cnt_6m,null,-1;pay_cinema_city_cnt_1y,null,-1;pay_cinema_city_cnt_td,null,-1;card_pay_ord_cnt_td,null,-1;card_pay_tkt_cnt_td,null,-1;presale_pay_ord_cnt_td,null,-1;discount_ord_cnt_td,null,-1;last_city_id,null,-1;last_city_level,null,-1;first_ticket_channel,null,-1;last_ticket_channel,null,-1;first_pay_diff,null,-1;last_pay_diff,null,-1;first_week_pay,null,-1;last_week_pay,null,-1;discount_amt_td,null,-1;free_ord_cnt_td,null,-1;single_tkt_ord_cnt_td,null,-1;pay_ord_cnt_1d,null,-1;pay_ord_cnt_3d,null,-1;pay_tkt_cnt_1d,null,-1;pay_tkt_cnt_3d,null,-1;pay_ord_amt_1d,null,-1;pay_ord_amt_3d,null,-1;card_pay_ord_cnt_1d,null,-1;card_pay_ord_cnt_3d,null,-1;card_pay_ord_cnt_1w,null,-1;card_pay_ord_cnt_2w,null,-1;card_pay_tkt_cnt_1d,null,-1;card_pay_tkt_cnt_3d,null,-1;card_pay_tkt_cnt_1w,null,-1;card_pay_tkt_cnt_2w,null,-1;presale_pay_ord_cnt_1d,null,-1;presale_pay_ord_cnt_3d,null,-1;presale_pay_ord_cnt_1w,null,-1;presale_pay_ord_cnt_2w,null,-1;bxo_1w,null,-1;bxo_2w,null,-1;bxo_1m,null,-1;bxo_2m,null,-1;bxo_3m,null,-1;bxo_6m,null,-1;bxo_1y,null,-1;show_type,null,-1;star_score,null,-1;is_reopen_ids,null,-1;sub_movie_type_id_ids,null,-1;language_ids,null,-1;produce_country_ids,null,-1;director_id_ids,null,-1;leading_role_id_1_ids,null,-1;leading_role_id_2_ids,null,-1;leading_role_id_3_ids,null,-1;film_producer_ids,null,-1;presenter_ids,null,-1;duration,null,-1;douban_rating,null,-1"
 -DoutputTableName="ytrec.ads_ykma_taopp_pointwise_features_fillna_rand_v2"
 -DoutputParaTableName="ytrec.ads_ykma_taopp_pointwise_features_para_v2"
 -DinputTableName="ytrec.ads_ykma_taopp_pointwise_features_rand_v2";











----------2\拆分---------------------------------------
drop table if exists ytrec.ads_ykma_taopp_pointwise_features_fillna_rand_1_v2;
drop table if exists ytrec.ads_ykma_taopp_pointwise_features_fillna_rand_2_v2;

PAI -name split -project algo_public -Dlifecycle="7"
 -Doutput1TableName="ytrec.ads_ykma_taopp_pointwise_features_fillna_rand_1_v2"
 -Doutput2TableName="ytrec.ads_ykma_taopp_pointwise_features_fillna_rand_2_v2"
 -DinputTableName="ytrec.ads_ykma_taopp_pointwise_features_fillna_rand_v2"
 -Dfraction="0.8";


-------------3\模型训练，PS-SMART---------------------------------------
drop table if exists ytrec.ads_ykma_taopp_pointwise_offline_model_imp_v2;
drop table if exists ytrec.ads_ykma_taopp_pointwise_offline_model_tmp_v2;
PAI -name ps_smart -project algo_public
  -DfeatureImportanceType="gain"
  -DlabelColName="label"
  -DoutputImportanceTableName="ytrec.ads_ykma_taopp_pointwise_offline_model_imp_v2"
  -DsampleRatio="0.8"
  -Dl1="5.0"
  -Dl2="1.0"
  -DfeatureRatio="0.8"
  -DtreeCount="100"
  -DbaseScore="0.5"
  -DminSplitLoss="0"
  -Dobjective="binary:logistic"
  -DfeatureNum="207"
  -DfeatureColNames="type_ids,pred_gender_ids,pred_age_level_ids,id_gender_ids,id_constellation_ids,pred_life_stage_hasbaby_ids,pred_life_stage_marriednochild_ids,id_zodiac_ids,pred_life_stage_marriedhaschild_ids,pred_life_stage_inlove_ids,pred_life_stage_married_ids,id_age,pred_life_stage_haschild_ids,pred_life_stage_ids,tm_level_ids,pred_life_stage_single_ids,vip_level_name_ids,pred_life_stage_marrying_ids,pred_is_undergraduate_ids,pred_education_degree_ids,pred_school_ids,pred_attending_college_ids,pred_career_type_ids,is_high_end_consumer_ids,pred_has_pet_ids,pred_has_car_ids,pred_has_house_ids,pred_car_series_ids,car_brand_ids,purchase_power_level_purchase_power_ids,ip_prov_name_ids,ip_city_name_ids,common_receive_city_code_180d_ids,common_receive_city_180d_ids,common_receive_province_id_gw_180d_ids,common_receive_province_gw_180d_ids,common_receive_city_level_gw_180d_ids,common_receive_district_id_gw_180d_ids,common_receive_district_gw_180d_ids,common_receive_city_code_gw_180d_ids,common_receive_city_id_gw_180d_ids,common_receive_city_name_gw_180d_ids,tkm_level_ids,tkm_level_title_ids,point_ids,is_has_eff_huabei_ids,is_has_eff_88card_ids,is_has_eff_card_ids,is_has_eff_citycard_ids,is_comm_master_ids,tq_level_ids,cate_id_ids,cate_name_ids,prefer_director_ids,prefer_actors_ids,prefer_type_ids,prefer_distributor_ids,prefer_country_ids,prefer_language_ids,prefer_version_ids,pred_car_brand_ids,card_pay_ord_cnt_1m,card_pay_ord_cnt_2m,card_pay_ord_cnt_3m,card_pay_ord_cnt_6m,card_pay_ord_cnt_1y,card_pay_tkt_cnt_1m,card_pay_tkt_cnt_2m,card_pay_tkt_cnt_3m,card_pay_tkt_cnt_6m,card_pay_tkt_cnt_1y,presale_pay_ord_cnt_1m,presale_pay_ord_cnt_2m,presale_pay_ord_cnt_3m,presale_pay_ord_cnt_6m,presale_pay_ord_cnt_1y,discount_ord_cnt_1m,discount_ord_cnt_2m,discount_ord_cnt_3m,discount_ord_cnt_6m,discount_ord_cnt_1y,pay_ord_cnt_1w,pay_ord_cnt_2w,pay_ord_cnt_1m,pay_ord_cnt_2m,pay_ord_cnt_3m,pay_ord_cnt_6m,pay_ord_cnt_1y,pay_ord_cnt_td,pay_ord_amt_1w,pay_ord_amt_2w,pay_ord_amt_1m,pay_ord_amt_2m,pay_ord_amt_3m,pay_ord_amt_6m,pay_ord_amt_1y,pay_ord_amt_td,pay_film_cnt_1w,pay_film_cnt_2w,pay_film_cnt_1m,pay_film_cnt_2m,pay_film_cnt_3m,pay_film_cnt_6m,pay_film_cnt_1y,pay_film_cnt_td,pay_cinema_cnt_1w,pay_cinema_cnt_2w,pay_cinema_cnt_1m,pay_cinema_cnt_2m,pay_cinema_cnt_3m,pay_cinema_cnt_6m,pay_cinema_cnt_1y,pay_cinema_cnt_td,pay_tkt_cnt_1w,pay_tkt_cnt_2w,pay_tkt_cnt_1m,pay_tkt_cnt_2m,pay_tkt_cnt_3m,pay_tkt_cnt_6m,pay_tkt_cnt_1y,pay_tkt_cnt_td,pay_tkt_sale_cnt_1w,pay_tkt_sale_cnt_2w,pay_tkt_sale_cnt_1m,pay_tkt_sale_cnt_2m,pay_tkt_sale_cnt_3m,pay_tkt_sale_cnt_6m,pay_tkt_sale_cnt_1y,pay_tkt_sale_cnt_td,pay_scd_cnt_1w,pay_scd_cnt_2w,pay_scd_cnt_1m,pay_scd_cnt_2m,pay_scd_cnt_3m,pay_scd_cnt_6m,pay_scd_cnt_1y,pay_scd_cnt_td,pay_scd_sale_cnt_1w,pay_scd_sale_cnt_2w,pay_scd_sale_cnt_1m,pay_scd_sale_cnt_2m,pay_scd_sale_cnt_3m,pay_scd_sale_cnt_6m,pay_scd_sale_cnt_1y,pay_scd_sale_cnt_td,pay_cinema_city_cnt_1w,pay_cinema_city_cnt_2w,pay_cinema_city_cnt_1m,pay_cinema_city_cnt_2m,pay_cinema_city_cnt_3m,pay_cinema_city_cnt_6m,pay_cinema_city_cnt_1y,pay_cinema_city_cnt_td,card_pay_ord_cnt_td,card_pay_tkt_cnt_td,presale_pay_ord_cnt_td,discount_ord_cnt_td,last_city_id,last_city_level,first_ticket_channel,last_ticket_channel,first_pay_diff,last_pay_diff,first_week_pay,last_week_pay,discount_amt_td,free_ord_cnt_td,single_tkt_ord_cnt_td,pay_ord_cnt_1d,pay_ord_cnt_3d,pay_tkt_cnt_1d,pay_tkt_cnt_3d,pay_ord_amt_1d,pay_ord_amt_3d,card_pay_ord_cnt_1d,card_pay_ord_cnt_3d,card_pay_ord_cnt_1w,card_pay_ord_cnt_2w,card_pay_tkt_cnt_1d,card_pay_tkt_cnt_3d,card_pay_tkt_cnt_1w,card_pay_tkt_cnt_2w,presale_pay_ord_cnt_1d,presale_pay_ord_cnt_3d,presale_pay_ord_cnt_1w,presale_pay_ord_cnt_2w,bxo_1w,bxo_2w,bxo_1m,bxo_2m,bxo_3m,bxo_6m,bxo_1y,show_type,star_score,is_reopen_ids,sub_movie_type_id_ids,language_ids,produce_country_ids,director_id_ids,leading_role_id_1_ids,leading_role_id_2_ids,leading_role_id_3_ids,film_producer_ids,presenter_ids,duration,douban_rating"
  -Dlifecycle="28"
  -DmaxDepth="5"
  -DmodelName="xlab_m_pai_ps_smart_b_6542680_v0"
  -DenableSparse="false"
  -Dmetric="auc"
  -DoutputTableName="ytrec.ads_ykma_taopp_pointwise_offline_model_tmp_v2"
  -DsketchEps="0.03"
  -DregardZeroAsMissing="false"
  -DinputTableName="ytrec.ads_ykma_taopp_pointwise_features_fillna_rand_1_v2"
  -Dshrinkage="0.1"
  -DcoreNum="100"
  -DmemSizePerCore="4096"
  -DserverNum="100"
  -DserverMemory="4096"
;



CREATE TABLE IF NOT EXISTS ytrec.ads_ykma_taopp_pointwise_offline_model_v2
(

	`id` BIGINT ,
	`value` BIGINT
)
PARTITIONED BY
(
    ds STRING
)
LIFECYCLE 7
;




INSERT OVERWRITE TABLE ytrec.ads_ykma_taopp_pointwise_offline_model_v2 PARTITION( ds='${bizdate}')
SELECT * FROM ytrec.ads_ykma_taopp_pointwise_offline_model_tmp_v2;

