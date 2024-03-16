pub use redis_om::HashModel;


#[derive(HashModel, Debug, PartialEq, Eq, Default)]
pub struct Customer {
    pub id: String,
    pub first_name: String,
    pub last_name: String,
    pub email: String,
    pub bio: Option<String>,
    pub interests: Vec<String>,
}

